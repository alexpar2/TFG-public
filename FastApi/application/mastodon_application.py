# # from persistence.mastodon_persistence import *
# # from models.mastodon import *
# # from config.connection import conmastodon
# from fastapi import HTTPException
# import json
# from config.connection import cancel_event  # Importar el evento de cancelación
# import threading
# from .comun_application import ThreadWithReturnValue  

# def get_all_mastodon():
#     """
#     Obtiene todos los registros de Mastodon de la base de datos.

#     Returns:
#         Lista de registros de Mastodon.
#     """
#     try:
#         data = get_all_mastodonDB()
#         accounts = data.get("accounts", [])
#         statuses = data.get("statuses", [])
#         hashtags = data.get("hashtags", [])

#         result = {
#             "accounts": json.loads(json.dumps(accounts, default=str)),
#             "statuses": json.loads(json.dumps(statuses, default=str)),
#             "hashtags": json.loads(json.dumps(hashtags, default=str))
#         }

#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching data from database: {str(e)}")
    


# def insert_mastodon(name: str, insertar: bool):
#     """
#     Inserta datos de Mastodon basados en una búsqueda por tema en la base de datos.

#     Args:
#         name: Término de búsqueda.
#         insertar: Booleano para determinar si se insertan los datos en la base de datos.
#     """
#     global cancel_event

#     # Resetear el evento de cancelación
#     cancel_event.clear()

#     def run_insertion():
#         try:
#             results = conmastodon.search_v2(name, resolve=True)
            
#             accounts = []
#             statuses = []
#             hashtags = []

#             def check_cancel_signal():
#                 if cancel_event.is_set():
#                     raise Exception("Proceso cancelado")

#             # Procesar cuentas
#             for account_data in results.get('accounts', []):
#                 check_cancel_signal()  # Verificar cancelación
#                 account_dict = {
#                     "id": account_data["id"],
#                     "username": account_data["username"],
#                     "acct": account_data["acct"],
#                     "display_name": account_data["display_name"],
#                     "locked": account_data["locked"],
#                     "bot": account_data["bot"],
#                     "discoverable": account_data["discoverable"],
#                     "indexable": account_data["indexable"],
#                     "group": account_data["group"],
#                     "created_at": account_data["created_at"],
#                     "note": account_data["note"],
#                     "url": account_data["url"],
#                     "uri": account_data["uri"],
#                     "avatar": account_data["avatar"],
#                     "avatar_static": account_data["avatar_static"],
#                     "header": account_data["header"],
#                     "header_static": account_data["header_static"],
#                     "followers_count": account_data["followers_count"],
#                     "following_count": account_data["following_count"],
#                     "statuses_count": account_data["statuses_count"],
#                     "last_status_at": account_data["last_status_at"],
#                     "hide_collections": account_data["hide_collections"],
#                     "emojis": account_data["emojis"],
#                     "fields": account_data["fields"]
#                 }
#                 accounts.append(account_dict)

#             # Procesar estados
#             for status_data in results.get('statuses', []):
#                 check_cancel_signal()  # Verificar cancelación
#                 status_dict = {
#                     "id": status_data["id"],
#                     "created_at": status_data["created_at"],
#                     "in_reply_to_id": status_data.get("in_reply_to_id"),
#                     "in_reply_to_account_id": status_data.get("in_reply_to_account_id"),
#                     "sensitive": status_data["sensitive"],
#                     "spoiler_text": status_data["spoiler_text"],
#                     "visibility": status_data["visibility"],
#                     "language": status_data["language"],
#                     "uri": status_data["uri"],
#                     "url": status_data["url"],
#                     "replies_count": status_data["replies_count"],
#                     "reblogs_count": status_data["reblogs_count"],
#                     "favourites_count": status_data["favourites_count"],
#                     "edited_at": status_data["edited_at"],
#                     "favourited": status_data["favourited"],
#                     "reblogged": status_data["reblogged"],
#                     "muted": status_data["muted"],
#                     "bookmarked": status_data["bookmarked"],
#                     "content": status_data["content"],
#                     "media_attachments": status_data["media_attachments"],
#                     "mentions": status_data["mentions"],
#                     "tags": status_data["tags"],
#                     "emojis": status_data["emojis"],
#                     "card": status_data["card"],
#                     "poll": status_data["poll"],
#                     "account_id": status_data["account"]["id"]  # Relación con la cuenta
#                 }
#                 statuses.append(status_dict)

#             # Procesar hashtags
#             for hashtag_data in results.get('hashtags', []):
#                 check_cancel_signal()  # Verificar cancelación
#                 hashtag_dict = {
#                     "name": hashtag_data["name"],
#                     "url": hashtag_data["url"],
#                     "history": hashtag_data["history"]
#                 }
#                 hashtags.append(hashtag_dict)

#             # Verificar si se encontraron resultados
#             if not accounts and not statuses and not hashtags:
#                 raise HTTPException(status_code=404, detail="No accounts, statuses, or hashtags found for the given search term.")

#             # Insertar en las bases de datos correspondientes si insertar es True
#             if insertar:
#                 check_cancel_signal()  # Verificar cancelación
#                 if accounts:
#                     insert_mastodon_accountsDB(accounts)
#                 check_cancel_signal()  # Verificar cancelación
#                 if statuses:
#                     insert_mastodon_statusesDB(statuses)
#                 check_cancel_signal()  # Verificar cancelación
#                 if hashtags:
#                     insert_mastodon_hashtagsDB(hashtags)

#             # Devolver todos los datos juntos
#             return {
#                 "accounts": accounts,
#                 "statuses": statuses,
#                 "hashtags": hashtags
#             }
            
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error processing Mastodon search: {str(e)}")

#     # Ejecutar el proceso de inserción en un hilo separado
#     insertion_thread = ThreadWithReturnValue(target=run_insertion)
#     insertion_thread.start()
#     result = insertion_thread.join()

#     # Verificar si la inserción fue cancelada
#     if cancel_event.is_set():
#         raise HTTPException(status_code=400, detail="Proceso cancelado")


#     return result
        
