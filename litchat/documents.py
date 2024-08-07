from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredXMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    TextLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel, model_validator
from langchain.docstore.document import Document
import os
import shutil
from typing import Any


class Paper(BaseModel):
    """Class contains paper metadata and derived quantities."""

    file_path: str
    docs: Any = None
    vdb: Any = None
    xml_extract: bool = False

    @model_validator(mode="before")
    @classmethod
    def set_arributes(cls, values):
        ## set default values
        defaults = {
            "chunk_size": 1000,
            "chunk_overlap": 50,
            "xml_extract": False,
            "docs": None,
            "vdb": None,
            "vect_dir": "./vectdb/",
            "embedding": None,
            "create_db": True,
        }
        for key, value in defaults.items():
            if key not in values:
                values[key] = value

        if values["docs"] == None:
            values["docs"] = cls.load_split_docs(
                filename=values["file_path"],
                chunk_size=values["chunk_size"],
                chunk_overlap=values["chunk_overlap"],
                xml_extract=values["xml_extract"],
            )
        if values["vdb"] == None:
            values["vdb"] = cls.vectorize_docs(
                docs_split=values["docs"],
                embedding=values["embedding"],
                vect_dir=values["vect_dir"],
                create_db=values["create_db"],
            )

        return values

    @classmethod
    def load_split_docs(
        cls, filename: str, chunk_size: int, chunk_overlap: int, xml_extract: bool
    ) -> list:
        # Identify file extension
        _, file_extension = os.path.splitext(filename)

        operations = {
            # Markups
            ".xml": lambda: UnstructuredXMLLoader(filename).load(),
            ".html": lambda: UnstructuredHTMLLoader(filename).load(),
            # Markdowns
            ".mmd": lambda: UnstructuredMarkdownLoader(filename).load(),
            ".md": lambda: UnstructuredMarkdownLoader(filename).load(),
            ".markdown": lambda: UnstructuredMarkdownLoader(filename).load(),
            # PDFs
            ".pdf": lambda: PyPDFLoader(filename).load(),
            # Text
            ".txt": lambda: TextLoader(filename, encoding="UTF-8").load(),
            # Docs remove for now
            # ".docx": lambda: UnstructuredWordDocumentLoader(filename).load(),
        }

        if xml_extract:
            assert (
                file_extension.lower() == ".xml"
            ), "XML extraction is only supported for XML files. Set xml_extract=False to disable."
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            # Extract title and abstract
            title = extract_text(content, '<title level="a" type="main">', "</title>")
            abstract = extract_text(content, "<abstract>", "</abstract>")
            body = extract_text(content, "<body>", "</body>")
            docs = Document(
                page_content=f"{title}\n{abstract}\n{body}",
                metadata={"source": filename},
            )
            docs = [docs]

        elif file_extension.lower() in operations:
            docs = operations[file_extension.lower()]()
        else:
            supported_extensions = ", ".join(operations.keys())
            raise ValueError(
                f"Unsupported file type: {file_extension}. Supported extensions are: {supported_extensions}"
            )

        # Split documents
        r_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )
        docs_split = r_splitter.split_documents(docs)

        return docs_split

    @classmethod
    def vectorize_docs(cls, docs_split: list, embedding: Any, **kwargs) -> None:
        vect_dir: str = kwargs.get("vect_dir", "./vectdb/")
        create_db: bool = kwargs.get("create_db", True)

        if embedding is None:
            # if you have an OPENAI API key, you can use the OpenAIEmbeddings class
            embedding = OpenAIEmbeddings()

        
        if create_db:
            if os.path.exists(vect_dir): 
                shutil.rmtree(vect_dir)
            os.makedirs(vect_dir)
            db = FAISS.from_documents(docs_split,embedding)
            db.save_local(folder_path=f"{vect_dir}/faiss_index")

        else:
            db = FAISS.load_local(vect_dir, embedding)
           
        return db
    
def extract_text(content, start_tag, end_tag):
    """Extract text between two specified tags in xml file."""
    start_index = content.find(start_tag)
    end_index = content.find(end_tag)
    if start_index != -1 and end_index != -1:
        return content[start_index + len(start_tag) : end_index].strip()
    return None
