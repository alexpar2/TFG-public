# from fastapi import APIRouter
# from fastapi.responses import JSONResponse
# from application.mastodon_application import *

# routermastodon = APIRouter()
# routermastodon.prefix = "/api" 

# @routermastodon.get("/mastodon")
# def list_mastodons():
#    result = get_all_mastodon()
#    return JSONResponse(content=result)



# @routermastodon.put("/mastodon/insert/{name}")
# def insertar_mastodon(name: str):
#     insert_mastodon(name, True)
#     return f"{name} insertado"
#    # return JSONResponse(content=result)

# @routermastodon.get("/mastodon/visualizar/{name}")
# def visualizar_mastodon(name: str):
#     result = insert_mastodon(name, False)
#     return result
#    # return JSONResponse(content=result)


