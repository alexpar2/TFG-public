from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from application.googlenews_application import *
from application.comun_application  import *

routergooglenews = APIRouter()
routergooglenews.prefix = "/api" 

@routergooglenews.get("/googlenews")
def list_gnewss():
   result = get_all_gnews()
   return JSONResponse(content=result)


@routergooglenews.put("/googlenews/insert/{name}")
def insertar_gnews(name: str):
    insert_gnews(name, True)
    return f"{name} insertado"
   # return JSONResponse(content=result)

@routergooglenews.get("/googlenews/visualizar/{name}")
def visualizar_gnews(name: str):
    result = insert_gnews(name, False)
    return result

#No implementado finalmente
# @routergooglenews.get("/googlenews/insertf/{tema}")
# def insertar_gnewsF(
#     tema : str,
#     fecha_ini: str = Query((datetime.now() - timedelta(days=1)).date(), description="Fecha de inicio en formato YYYY-MM-DD"),
#     fecha_hasta: str = Query((datetime.now()).date(), description="Fecha de inicio en formato YYYY-MM-DD")
# ):
#     fecha_ini_real = validate_date(fecha_ini)
#     fecha_hasta_real = validate_date(fecha_hasta)
#     result = insert_gnewsF(tema, fecha_ini_real ,fecha_hasta_real)
#     if result is not None:
#         return f"{tema} no encontrado"
#     else:
#         return f"{tema} insertado"

#Genera contenido anteriormente implmementado pero no usado finalmente
# @routergooglenews.get("/googlenews/contenido")
# def obtener_contenido(
#     id : str
# ):
#     post_id = ObjectId(id)
#     result = f"Contenido update"
#     result = obtener_contenido_id(post_id)
#     return result


#Obtiene url no usado finalmente
# @routergooglenews.get("/googlenews/url")
# def obtener_contenido(
#     id : str
# ):
#     post_id = ObjectId(id)
#     result = f"Url"
#     result = obtener_url_id(post_id)
#     return result

#Igual que el de abajo pero sin poder elegir la cantidad
# @routergooglenews.get("/googlenews/insertSecure/")
# def insertar_gnewsSecure(
#     fecha_ini: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}"),
#     fecha_hasta: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}")
# ):
#     insert_gnewsSecure(fecha_ini ,fecha_hasta)
#     return f"Noticias webs seguras insertadas"


@routergooglenews.put("/googlenews/insertSecure/list")
def insertar_gnewsSecure(
    fecha_ini: str = Query((datetime.now() - timedelta(days=1)).date(), description="Fecha de inicio en formato YYYY-MM-DD"),
    fecha_hasta: str = Query((datetime.now()).date(), description="Fecha de inicio en formato YYYY-MM-DD"),
    cantidad_webs_seguras : int = Query( 3, description="Numero de webs donde sacar inforamción", ge=1, le=len(list_of_trusted_sources)),
    # lista : list[str] = Query(list_of_trusted_sources, description="Fuentes confiables"),
    # lista2 : list[str] = list_of_trusted_sources,
    # json_schema_extra: dict = {
    #     "fuentes_seguras": {
    #         "description": "Lista de fuentes de noticias seguras",
    #         "lista": list_of_trusted_sources
    #     }
    # }
):
    
    fecha_ini_real = validate_date(fecha_ini)
    fecha_hasta_real = validate_date(fecha_hasta)
    result = insert_gnewsSecureCantidad(fecha_ini_real ,fecha_hasta_real, cantidad_webs_seguras)

    return f"Insertadas correctamennte"


@routergooglenews.post("/googlenews/insertCustomSources")
def insertar_gnews_custom(
    request: CustomSourcesRequest,
    fecha_ini: str = Query((datetime.now() - timedelta(days=1)).date(), description="Fecha de inicio en formato YYYY-MM-DD"),
    fecha_hasta: str = Query((datetime.now()).date(), description="Fecha de inicio en formato YYYY-MM-DD"),
):
    fecha_ini_real = validate_date(fecha_ini)
    fecha_hasta_real = validate_date(fecha_hasta)
    result = insert_gnews_custom_sources(fecha_ini_real, fecha_hasta_real, request.sources)
    return {"result": "Insertadas correctamente", "fuentes_sin_contenido": result}

