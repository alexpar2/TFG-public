from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from application.reddit_application import get_reddit_default, insert_reddits, insert_reddits_coment, get_all_reddits


routerreddit = APIRouter()
routerreddit.prefix = "/api" 

@routerreddit.get("/reddit")
def list_gnewss():
   result = get_all_reddits()
   return JSONResponse(content=result)



# @routerreddit.put("/reddit/insert/{name}")
# def insertar_reddits(name: str):
#     insert_reddits(name)
#     return f"{name} insertado"
#    # return JSONResponse(content=result)


@routerreddit.put("/reddit/insertComent/{tema}")
def insertar_reddits_commentario(
    tema: str,
    profundidad : int = Query( 1, description="Profundida de comentario", ge=0, le=3), 
    cantidad : int = Query( 3, description="Cantidad de reddits", ge=1),
    cantidad_nodo : int = Query( 3, description="Cantidad de comentarios por nodo", ge=0)
    ):
    result = insert_reddits_coment(tema, cantidad, profundidad, cantidad_nodo, True)
    return result



@routerreddit.get("/reddit/VisualizarComent/{tema}")
def visualizar_reddits_commentario(
    tema: str,
    profundidad : int = Query( 1, description="Profundida de comentario", ge=0, le=3), 
    cantidad : int = Query( 3, description="Cantidad de reddits", ge=1, le=20),
    cantidad_nodo : int = Query( 3, description="Cantidad de comentarios por nodo", ge=0)
    ):
    result = insert_reddits_coment(tema, cantidad, profundidad, cantidad_nodo, False)
    return result

