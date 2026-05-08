from pydantic import BaseModel,Field
from typing import List,Literal


class Message(BaseModel):
    role: str
    content: str



# Request model

class QueryRequest(BaseModel):
    query:str=Field(...,min_length=3,description="the user's healthcare questions")
    history:List[Message]=Field(default_factory=list)

#response model
class Source(BaseModel):
    document:str=Field(...,description="The name of the source document")
    chunk:str=Field(...,description="The relavant text snippet used for the answer")
    
class QueryResponse(BaseModel):
    answer:str=Field(...,description="The generated response from the AI")
    source:List[Source]=Field(default_factory=list,description="List of source citation")
    confidence:Literal['low','medium','high']=Field(...,description="The system's confidence in the answer")

class IngestionResponse(BaseModel):
    status:str
    documents_processed:int
    message:str
