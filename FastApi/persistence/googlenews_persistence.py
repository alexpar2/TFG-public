from fastapi import HTTPException
from config.connection import conn
from bson import ObjectId
from models.googlenews import *

def get_all_gnewsDB():

   try:
     return conn.TFG.GoogleNews.find()
   except Exception as ints:
    raise HTTPException(status_code=500, detail={"type":ints.__doc__,
                                                 "error":ints.args })

   

   
def insert_gnewsDB(posts: list[GNew]):
    """
    Inserta una lista de noticias de Google News en la base de datos.

    Args:
        posts: Lista de objetos de tipo GNew.
    """
    try:
        for post in posts:
            if conn.TFG.GoogleNews.count_documents({"url": post.url}, limit=1) == 0:
                conn.TFG.GoogleNews.insert_one(post.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})
    
    
def insert_gnewsNoContentDB(posts:list[GNew]):

  try:
    result = conn.TFG.GoogleNews.insert_many([post.dict() for post in posts])
    #return str(result.inserted_id)
  except Exception as ints:
   raise HTTPException(status_code=500, detail={"type":ints.__doc__,
                                                "error":ints.args })
  


def obtener_url_por_id(post_id):
  try:
      # Suponiendo que `conn.TFG.GoogleNews` es tu colección
      post = conn.TFG.GoogleNews.find_one({"_id": post_id})
      if post:
          return post.get("url")
      else:
          return f"No se encontró ningún post con el ID {post_id}."
  except Exception as e:
      raise HTTPException(status_code=500, detail={"type": str(type(e).__name__), "error": str(e)})
  

def update_content_in_gnewsDB(post_id, new_content):
    try:
        # Suponiendo que `conn.TFG.GoogleNews` es tu colección
        result = conn.TFG.GoogleNews.update_one({"_id": post_id}, {"$set": {"content": new_content}})
        if result.modified_count > 0:
            return f"El contenido del post con ID {post_id} se actualizó correctamente."
        else:
            return f"No se realizaron cambios en el contenido del post con ID {post_id}."
    except Exception as e:
        raise HTTPException(status_code=500, detail={"type": str(type(e).__name__), "error": str(e)})
