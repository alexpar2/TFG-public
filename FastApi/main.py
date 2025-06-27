from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from controllers.reddit_controller import *
from controllers.googlenews_controller import *
# from controllers.mastodon_controller import *
from application.analysis_application import *
import praw
from config.connection import cancel_event

import requests

   # https://docs.python.org/3/library/json.html
# This library will be used to parse the JSON data returned by the API.
import json
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request


#Mastodon
# from mastodon import Mastodon


#GNEWS biblioteca
from gnews import GNews
from datetime import datetime
# import newspaper


app = FastAPI()



from config.connection import create_unique_indexes
# Crear índices únicos al iniciar la aplicación
create_unique_indexes()

origins = [
   "*"
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials = True,
   allow_methods=["*"],
   allow_headers=["*"]
)


@app.get("/")
def read_root():
   return f'Root'

app.include_router(routerreddit, tags=["Métodos Reddit"])

app.include_router(routergooglenews, tags=["Métodos Google"])

app.include_router(routeranalysis, tags=["Métodos análisis"])

# app.include_router(routermastodon, tags=["Métodos Mastodon"])


from fastapi.responses import StreamingResponse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
from starlette.responses import Response



@app.get("/tag_cloud/{data}/{max_words}")
def create_tag_cloud(data: str, max_words: int):
    try:
        # Crear el WordCloud
        wordcloud = WordCloud(
            margin=2,
            width=500,
            height=400,
            max_font_size=100,
            max_words=int(max_words),
            background_color="white",
            collocations=False,
        ).generate(data)

        # Configurar la figura
        plt.figure(1)
        plt.figure(1).clear()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.tight_layout(pad=0)
        plt.axis("off")

        # Convertir la figura a PNG
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




from application.comun_application import *


@app.put("/api/cancel")
def cancel_insertion():
    cancel_event.set()
    return {"message": "Insertion process cancelled"}



    

    
from application.comun_application import *
@app.post("/generate_tag_cloud/",
    summary="Procesa una cadena de texto aplicando una serie de técnicas de preprocesamiento de texto.",
    description="""    
    El endpoint `preprocess_text` procesa una cadena de texto aplicando una serie de técnicas de preprocesamiento de texto. El endpoint toma los siguientes parámetros:

- `text` (str): El texto de entrada a ser preprocesado.
- `numbers` (str): Determina si se eliminan o reemplazan los números en el texto. Si se establece en `'noapply'`, los números no se modifican. Si se establece en un valor de cadena, todos los números en el texto se reemplazan con la cadena proporcionada.
- `caps` (str): Determina si se convierte el texto a minúsculas o mayúsculas. Si se establece en `'lowercase'`, el texto se convierte a minúsculas. Si se establece en `'uppercase'`, el texto se convierte a mayúsculas. Si se establece en cualquier otro valor, el texto no se modifica.
- `hashtags` (str): Determina si se eliminan o reemplazan los hashtags del texto. Si se establece en `'noapply'`, los hashtags no se modifican. Si se establece en un valor de cadena, todos los hashtags en el texto se reemplazan con la cadena proporcionada.
- `urls` (str): Determina si se eliminan o reemplazan las URLs del texto. Si se establece en `'noapply'`, las URLs no se modifican. Si se establece en un valor de cadena, todas las URLs en el texto se reemplazan con la cadena proporcionada.
- `mentions` (str): Determina si se eliminan o reemplazan las menciones del texto. Si se establece en `'noapply'`, las menciones no se modifican. Si se establece en un valor de cadena, todas las menciones en el texto se reemplazan con la cadena proporcionada.
- `stopwords_l` (str): Determina el conjunto de palabras vacías a usar. Si se establece en `'english'` o `'en'`, la función utiliza el conjunto de palabras vacías en inglés proporcionado por el Natural Language Toolkit (nltk).
- `lemmatize` (bool): Determina si se lematiza el texto utilizando el lematizador WordNet proporcionado por la biblioteca nltk.
- `stemming` (bool): No implementado en la versión actual.
- `punctuation` (bool): Determina si se eliminan todas las marcas de puntuación del texto.
- `tags` (bool): Determina si se aplica etiquetado de partes del discurso al texto utilizando la función `pos_tag()` proporcionada por la biblioteca nltk.

*Retorna*:
        list: La lista tokenizada modificada.""", 
    tags=["Métodos Generales"])
async def preprocess_text_endpoint(text : str = Query(..., description="El texto de entrada a ser preprocesado.", title="TextID"), 
               max_words: int = Query(100, description="Máximo número de palabras para el word cloud"),
               numbers : str = '', 
               caps : str = 'lowercase', hashtags : str = 'noapply',
               urls : str = 'noapply', mentions : str = 'noapply',
               stopwords_l: str = 'english', 
               lemmatize : bool = True, stemming : bool = False, 
               punctuation : bool = True, tags : bool = False):
    try:
        data = preprocess_text(text, numbers, caps, hashtags, urls, mentions, stopwords_l, lemmatize, stemming, punctuation, False)

        data2 =  " ".join(data)
    # Crear el WordCloud
        wordcloud = WordCloud(
            margin=2,
            width=500,
            height=400,
            max_font_size=100,
            max_words=max_words,
            background_color="white",
            collocations=False,
        ).generate(data2)

        # Configurar la figura
        plt.figure(1)
        plt.figure(1).clear()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.tight_layout(pad=0)
        plt.axis("off")

        # Convertir la figura a PNG
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    


    # @app.post("/preprocess_text/",
#     summary="Procesa una cadena de texto aplicando una serie de técnicas de preprocesamiento de texto.",
#     description="""    
#     El endpoint `preprocess_text` procesa una cadena de texto aplicando una serie de técnicas de preprocesamiento de texto. El endpoint toma los siguientes parámetros:

# - `text` (str): El texto de entrada a ser preprocesado.
# - `numbers` (str): Determina si se eliminan o reemplazan los números en el texto. Si se establece en `'noapply'`, los números no se modifican. Si se establece en un valor de cadena, todos los números en el texto se reemplazan con la cadena proporcionada.
# - `caps` (str): Determina si se convierte el texto a minúsculas o mayúsculas. Si se establece en `'lowercase'`, el texto se convierte a minúsculas. Si se establece en `'uppercase'`, el texto se convierte a mayúsculas. Si se establece en cualquier otro valor, el texto no se modifica.
# - `hashtags` (str): Determina si se eliminan o reemplazan los hashtags del texto. Si se establece en `'noapply'`, los hashtags no se modifican. Si se establece en un valor de cadena, todos los hashtags en el texto se reemplazan con la cadena proporcionada.
# - `urls` (str): Determina si se eliminan o reemplazan las URLs del texto. Si se establece en `'noapply'`, las URLs no se modifican. Si se establece en un valor de cadena, todas las URLs en el texto se reemplazan con la cadena proporcionada.
# - `mentions` (str): Determina si se eliminan o reemplazan las menciones del texto. Si se establece en `'noapply'`, las menciones no se modifican. Si se establece en un valor de cadena, todas las menciones en el texto se reemplazan con la cadena proporcionada.
# - `stopwords_l` (str): Determina el conjunto de palabras vacías a usar. Si se establece en `'english'` o `'en'`, la función utiliza el conjunto de palabras vacías en inglés proporcionado por el Natural Language Toolkit (nltk).
# - `lemmatize` (bool): Determina si se lematiza el texto utilizando el lematizador WordNet proporcionado por la biblioteca nltk.
# - `stemming` (bool): No implementado en la versión actual.
# - `punctuation` (bool): Determina si se eliminan todas las marcas de puntuación del texto.
# - `tags` (bool): Determina si se aplica etiquetado de partes del discurso al texto utilizando la función `pos_tag()` proporcionada por la biblioteca nltk.

# *Retorna*:
#         list: La lista tokenizada modificada.""", 
#     tags=["Métodos Generales"])
# async def preprocess_text_endpoint(text : str = Query(..., description="El texto de entrada a ser preprocesado.", title="TextID"), 
#                numbers : str = '', 
#                caps : str = 'lowercase', hashtags : str = 'noapply',
#                urls : str = 'noapply', mentions : str = 'noapply',
#                stopwords_l: str = 'english', 
#                lemmatize : bool = True, stemming : bool = False, 
#                punctuation : bool = True, tags : bool = False):
#     data = preprocess_text(text, numbers, caps, hashtags, urls, mentions, stopwords_l, lemmatize, stemming, punctuation, tags)
#     return data
#     return " ".join(data)

# #aborto de peticiones
# from threading import Lock
# # Variable global y su bloqueo para la señalización de cancelación
# from config.config import cancel_signal, cancel_lock