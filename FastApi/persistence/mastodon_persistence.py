# from fastapi import HTTPException
# from config.connection import conn
# from bson import ObjectId
# from models.mastodon import *
# from fastapi import HTTPException
# from config.connection import conn

# def get_all_mastodonDB():
#     """
#     Obtiene la unión de todos los registros de cuentas, estados y hashtags de Mastodon de la base de datos.

#     Returns:
#         Lista de diccionarios que contienen la unión de los registros de las tres colecciones.
#     """
#     try:
#         accounts_cursor = conn.TFG.Mastodon_accounts.find()
#         statuses_cursor = conn.TFG.Mastodon_statuses.find()
#         hashtags_cursor = conn.TFG.Mastodon_hashtags.find()
        
#         accounts = list(accounts_cursor)
#         statuses = list(statuses_cursor)
#         hashtags = list(hashtags_cursor)

#         result = {
#             "accounts": accounts,
#             "statuses": statuses,
#             "hashtags": hashtags
#         }

#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})


# def insert_mastodonDB(posts:list):
#   """
#     Inserta una lista de cuentas de Mastodon en la base de datos.

#     Args:
#         accounts: Lista de objetos de tipo Account.
#   """

#   try:
#     result = conn.TFG.Mastodon.insert_many(posts)
#     #return str(result.inserted_id)
#   except Exception as ints:
#     raise HTTPException(status_code=500, detail={"type":ints.__doc__,
#                                                 "error":ints.args })
  
# from fastapi import HTTPException
# from config.connection import conn

# def insert_mastodon_accountsDB(accounts: list):
#     """
#     Inserta una lista de cuentas de Mastodon en la base de datos.

#     Args:
#         accounts: Lista de diccionarios con información de cuentas.
#     """
#     try:
#         for account in accounts:
#             if conn.TFG.Mastodon_accounts.count_documents({"id": account["id"]}, limit=1) == 0:
#                 conn.TFG.Mastodon_accounts.insert_one(account)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})

# def insert_mastodon_statusesDB(statuses: list):
#     """
#     Inserta una lista de estados de Mastodon en la base de datos.

#     Args:
#         statuses: Lista de diccionarios con información de estados.
#     """
#     try:
#         for status in statuses:
#             if conn.TFG.Mastodon_statuses.count_documents({"id": status["id"]}, limit=1) == 0:
#                 conn.TFG.Mastodon_statuses.insert_one(status)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})

# def insert_mastodon_hashtagsDB(hashtags: list):
#     """
#     Inserta una lista de hashtags de Mastodon en la base de datos.

#     Args:
#         hashtags: Lista de diccionarios con información de hashtags.
#     """
#     try:
#         for hashtag in hashtags:
#             if conn.TFG.Mastodon_hashtags.count_documents({"name": hashtag["name"]}, limit=1) == 0:
#                 conn.TFG.Mastodon_hashtags.insert_one(hashtag)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})



# # from fastapi import HTTPException
# # from config.connection import conn
# # from models.mastodon import Account



# # def insert_mastodonDB(accounts: list):
# #     """
# #     Inserta una lista de cuentas de Mastodon en la base de datos.

# #     Args:
# #         accounts: Lista de objetos de tipo Account.
# #     """
# #     try:
# #         result = conn.TFG.Mastodon.insert_many([account.dict() for account in accounts])
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args })



   