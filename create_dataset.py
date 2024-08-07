from extract_data import run_extractor

"""setup questions as you want. Be as specific as possible. 
The more specific the question, the better the answer will be. Few examples are given below."""

## Add your questions here. Fw examples are given below. 
questions = [
            "what are the toxicological properties of ketene?", 
             "What causes EVALI?"
             ]

filedir =  "path/to/your/pdf/files"
data_dir = "litchat/outputdir"  # "path/to/your/output/directory"  # everything will be saved here. Make sure this folder exists
chunk_size = 500  # change this value as needed. This is the number of words in small "paragraphs" that the model will read at a time
chunk_overlap = 50  # change this value as needed. This is the number of words that will overlap between each "paragraph"
add_previous = False  # if True, the previous question and answer will be added to the context of the next question
create_db = True  # if True, the vector database will be created. If False, it will use the existing database
vect_dir = "litchat/vectdb/"  # "path/to/your/vector/database"  # if you have created the vector database before. In this case set create_db = False. 

run_extractor(
    filedir,
    questions,
    data_dir,
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    add_previous=add_previous,
    create_db=create_db,
    vect_dir = vect_dir #if create_db is False and you have a vector database already created!
)
