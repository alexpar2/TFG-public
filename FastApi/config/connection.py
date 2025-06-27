from pymongo import MongoClient, ASCENDING
import praw
# from mastodon import Mastodon
from gnews import GNews
from fastapi import HTTPException


import os

# # Cliente Mongo docker
mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017')  # usar el nombre del servicio de MongoDB

try:
    conn = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # Timeout después de 5 segundos
    # Probar la conexión
    conn.admin.command('ping')
    print("Conexión a MongoDB establecida.")
except Exception as e:
    conn = None
    print("No se pudo conectar a MongoDB: ", e)





def create_unique_indexes():
    if conn is not None:
        try:
            # Crear índices únicos para las colecciones relevantes
            # conn.TFG.Mastodon_accounts.create_index([("id", ASCENDING)], unique=True)
            # conn.TFG.Mastodon_statuses.create_index([("id", ASCENDING)], unique=True)
            # conn.TFG.Mastodon_hashtags.create_index([("name", ASCENDING)], unique=True)
            conn.TFG.GoogleNews.create_index([("url", ASCENDING)], unique=True)  # Asumiendo que 'url' es único para cada noticia
            conn.TFG.reddit.create_index([("ID", ASCENDING)], unique=True)  # Asumiendo que 'ID' es único para cada post de Reddit
            print("Índices únicos creados/verificados exitosamente.")
        except Exception as e:
            raise HTTPException(status_code=500, detail={"type": e.__doc__, "error": e.args})
    else:
        print("Conexión a MongoDB no encontrada. No se crearon índices únicos.")





conreddit = praw.Reddit(
   client_id='xxxxxx', client_secret='xxxxxx',
                         user_agent='xxxxxx', username="xxxxxx",
                         password="xxxxxx"
)

#apii google news

apikeygnews = "xxxxxx"

#Con biblioteca
google_news = GNews(max_results=100)
# google_news1 = GNews(max_results=1)



#Mastodon.py

# conmastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
# conmastodon.log_in(
#     'e.vilarperez@go.ugr.es',
#     'KydCgcaRJ.854jr',
#     to_file = 'pytooter_usercred.secret'
# )


#cancelar
from threading import Event

cancel_event = Event()
