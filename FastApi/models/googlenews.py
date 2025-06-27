from pydantic import BaseModel

class GNewId(BaseModel):
   id:str

class GNew(BaseModel):
   Title:str
   MediaName:str
   content:str
   url:str



class CustomSourcesRequest(BaseModel):
    sources: list[str]