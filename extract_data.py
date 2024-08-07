import os
from langchain.llms import Ollama
from litchat.utils import get_parsers, get_prompted_model, get_writers, get_field_names
from litchat.prompts import QAPROMPT
from litchat.parsers import QAPARSER
from litchat.documents import Paper
from langchain.embeddings import HuggingFaceEmbeddings

## set language model and embeddings
embedding_model = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}  # use "cuda" if you have a GPU
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model, model_kwargs=model_kwargs
)

# language model = mistral. But you can use any model in Ollama
llm = Ollama(model="mistral", temperature=0)
## add gpt for future use
output_parser = get_parsers(QAPARSER)
input_variables = [
    "question",
    "chunks",
    "previous",
]  # these are the extact names within {} in the prompt
llm_chain = get_prompted_model(
    llm=llm, prompt=QAPROMPT, input_variables=input_variables, parser=output_parser
)  # this is the final "chat" model


def run_extractor(filedir, questions, data_dir="litchat/outputdir", **kwargs):
    chunk_size = kwargs.get("chunk_size", 500)
    chunk_overlap = kwargs.get("chunk_overlap", 50)
    vect_dir = kwargs.get("vect_dir", "litchat/vectdb/")
    create_db = kwargs.get("create_db", True)
    add_previous = kwargs.get("add_previous", False)

    # headers for the csv file. This method automatically generates headers based on the number of questions
    # eg: ["filename", "Q1", "A1", "Context_used_1"... "Qn", "An", "Context_used_n"]
    field_names = get_field_names(n=len(questions))

    # get the writers for the log, error and csv files
    logwriter, errorwriter, dictwriter, csvwriter = get_writers(
        datadir=data_dir, field_names=field_names
    )

    for file in os.listdir(filedir):
        row = {}
        row["filename"] = file

        # Paper class is used to parse pdfs and create a vector database
        paper = Paper(
            file_path=os.path.join(filedir, file),
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding=embeddings,
            vect_dir=vect_dir,
            create_db=create_db,  # set to False if you're using the same files again and again.
        )
        previous = ""  # only needed if there are multiple questions and questions are dependent on each other
        for i, question in enumerate(questions):
            retrieved_text = paper.vdb.similarity_search(question, k=3)

            response = llm_chain.invoke(
                {"question": question, "chunks": retrieved_text, "previous": previous}
            )
            try:
                response = output_parser.invoke(response).dict()

            except Exception:
                response = {"answer": "Not Found", "context": "Not Found"}
                errorwriter.write(f"Error processing: {file} - question {i+1}\n")

            ## fields have to be in the field_names list
            row[f"Question_{i+1}"] = question
            row[f"Answer_{i+1}"] = response["answer"]
            row[f"Context_used_{i+1}"] = response["context"]
            if add_previous:
                previous += f"Q: {question}\nA: {response['answer']}\n"
                print(previous)

        logwriter.write(f"Processed: {file}\n")

        dictwriter.writerow(row)
    logwriter.close()
    csvwriter.close()
    errorwriter.close()
