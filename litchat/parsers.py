from langchain.pydantic_v1 import BaseModel, Field

class QAPARSER(BaseModel):
    answer: str = Field(..., description="answer to question")
    context: str = Field(..., description="context used for answer")
