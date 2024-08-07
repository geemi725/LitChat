import os
from langchain.llms import Ollama
from langchain.pydantic_v1 import BaseModel, Field
from .utils import get_parsers
from langchain_core.prompts.prompt import PromptTemplate


filedir = "/data/share/scientific_publications/chemrxiv_grobid_out/"

CLUSTER_PROMPT = """Given the following scientific title and abstract, what is the most likely cluster label from the given list?
The cluster label must be one from the provided list of cluster labels only. If you cannot find a suitable cluster label, please select label 'Unclassified'.
Title: {title}
Abstract: {abstract}
Cluster Labels: {cluster_labels}

Format instructions: \n{format_instructions}
"""


class ClusterLabel(BaseModel):
    cluster_label: str = Field(..., description="cluster label")


def extract_text(element, start_tag, end_tag):
    start_index = element.find(start_tag)
    end_index = element.find(end_tag)
    if start_index != -1 and end_index != -1:
        return element[start_index + len(start_tag) : end_index].strip()
    return ""





llm = Ollama(model="mistral", temperature=0)
cluster_parser = get_parsers(ClusterLabel)

llm_chain = prompted_model(
    llm, CLUSTER_PROMPT, ["title", "abstract", "clusters"], cluster_parser
)

## main loop
# # Iterate through all XML files in the filedir
for filename in os.listdir(filedir):
    if filename.endswith(".xml"):
        file_path = os.path.join(filedir, filename)

        # Read the file content as text
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Extract title and abstract
        title = extract_text(content, '<title level="a" type="main">', "</title>")
        abstract = extract_text(content, "<abstract>", "</abstract>")
        if not title or not abstract:
            continue
        # Generate the response
        response = llm_chain.invoke(
            {"title": title, "abstract": abstract, "cluster_labels": mega_clusters}
        )
        try:
            response = cluster_parser.invoke(response).dict()
        except:
            response = {"cluster_label": "Unclassified"}

        with open(
            f"clusters_mistral/{response['cluster_label'].lower()}.txt", "a+"
        ) as f:
            f.write(filename + "\n")
        f.close()
