from fastapi import HTTPException
from config.connection import conn
from bson import ObjectId
from models.reddit import *

def get_all_redditsDB():

   try:
     return conn.TFG.reddit.find()
   except Exception as ints:
    raise HTTPException(status_code=500, detail={"type":ints.__doc__,
                                                 "error":ints.args })
def insert_reddictsDB(posts: list[RedditPost]):
    """
    Inserta una lista de posts de Reddit en la base de datos.

    Args:
        posts: Lista de objetos de tipo RedditPost.
    """
    try:
        for post in posts:
            if conn.TFG.reddit.count_documents({"ID": post.ID}, limit=1) == 0:
                conn.TFG.reddit.insert_one(post.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})
  
def insert_reddicts2DB(posts: list[RedditPost]):
    """
    Inserta una lista de posts de Reddit en la base de datos.

    Args:
        posts: Lista de objetos de tipo RedditPost.
    """
    try:
        for post in posts:
            if conn.TFG.reddit.count_documents({"ID": post.ID}, limit=1) == 0:
                conn.TFG.reddit.insert_one(post.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})
  

def insert_reddictsoneDB(post:Reddit):
   try:
        result = conn.TFG.reddit.insert_one(post)
        #return str(result.inserted_id)
   except Exception as ints:
    raise HTTPException(status_code=500, detail={"type":ints.__doc__,
                                                    "error":ints.args })
    
# def get_productDB(product_id):

#   try:
#     query = {"_id": ObjectId(product_id)}
#     result = conn.TFG.reddit.find_one(query)
#     return result
#   except Exception as ints:
#    raise HTTPException(status_code=500, detail={"type":ints.__doc__,
#                                                 "error":ints.args })  