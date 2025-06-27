from pydantic import BaseModel

class RedditId(BaseModel):
   id:str

class Reddit(BaseModel):
   Title:str
   ID:str
   Author:str
   URL:str
   Score:float
   Karma:str



class RedditComment(BaseModel):
    Body: str
    Author: str
    Replies: list['RedditComment'] = []

class RedditPost(BaseModel):
    Title: str
    ID: str
    Author: str
    URL: str
    Score: float
    Karma: str
    Comments: list[RedditComment]