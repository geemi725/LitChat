from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts.prompt import PromptTemplate
import os
from typing import Any
from csv import DictWriter

def get_parsers(parserobj: Any):
    parser = PydanticOutputParser(pydantic_object=parserobj)
    return parser

def get_prompted_model(llm, prompt, input_variables, parser):
    prompt_template = PromptTemplate(
        template=prompt,
        input_variables=input_variables,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt_template | llm

def get_writers(field_names, **kwargs):
        datadir = kwargs.get("datadir", "data")
        logfile = kwargs.get("logfile",f"{datadir}/log_file.txt")
        csvfile = kwargs.get("csvfile",f"{datadir}/dataset.csv")
        errorfile = kwargs.get("errorfile",f"{datadir}/error_file.txt")

        logwriter = open(logfile, "w+")

        if os.path.exists(csvfile):
            writeheader = False
        else:
            writeheader = True
        csvwriter = open(csvfile, "a")
        errorwriter = open(errorfile, "w+")

        dictwriter = DictWriter(csvwriter, fieldnames=field_names)
        if writeheader: dictwriter.writeheader()

        return logwriter, errorwriter, dictwriter, csvwriter

def get_field_names(n):
    # Start with the 'paper' in the list
    field_names = ['filename']
    
    for i in range(1, n + 1):
        field_names.append(f"Question_{i}")
        field_names.append(f"Answer_{i}")
        field_names.append(f"Context_used_{i}")
    
    return field_names
