# analysis_application.py
"""
FastAPI endpoints for Reddit topic analysis, news correlation, explanations, and fake news detection.

- /api/Search/{search}: Busca un subreddit, analiza tópicos y sentimientos.
- /api/news: Devuelve noticias relacionadas con un tópico.
- /api/explanation: Explicación LLM sobre el tópico y noticias.
- /api/fakenews: Evalúa si un texto es fake news (modelo + LLM).
- /api/analyze: Analiza una lista de párrafos (tópicos y sentimientos).
"""

#Librerías estándar

import os
import re
import json
import warnings
from collections import Counter

#Third-party

import praw
import numpy as np
import asyncpraw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from fastapi import Response
from sklearn.feature_extraction.text import CountVectorizer
import random
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from umap.umap_ import UMAP
from sklearn.cluster import DBSCAN
import plotly.express as px
from fastapi.responses import HTMLResponse
from openai import OpenAI
from prawcore import NotFound
from newsapi import NewsApiClient
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

warnings.simplefilter(action='ignore', category=FutureWarning)

random.seed(12456)

topicos = []
routeranalysis = APIRouter()
routeranalysis.prefix = "/analysis"

@routeranalysis.get("/api/Search/{search}")
async def search(search: str, stmodel: str = Query("all-mpnet-base-v2", description="Model to use")):
    """
    Busca un subreddit, analiza los posts para extraer tópicos y sentimientos.
    Devuelve los tópicos principales y el conteo de sentimientos.
    """
    global topicos

    reddit = praw.Reddit(client_id='xxxxxx', client_secret='xxxxxx',
                         user_agent='xxxxxx', username="xxxxxx",
                         password="xxxxxx")

    asyncreddit = asyncpraw.Reddit(client_id='xxxxxx', client_secret='xxxxxx',
                                   user_agent='xxxxxx', username="xxxxxx",
                                   password="xxxxxx")

    def sub_exists(sub):
        # Comprueba si existe el subreddit
        exists = True
        try:
            reddit.subreddits.search_by_name(sub, exact=True)
        except:
            exists = False
        return exists

    if sub_exists(search) == True:
        posts = []
        ml_subreddit = await asyncreddit.subreddit(search)
        async for post in ml_subreddit.hot(limit=None):
            posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext,
                          post.created])
        postsSience = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

    else:

        error_message = 'The subreddit ' + search + ' doesn´t exist'
        return error_message


    frame = pd.DataFrame(postsSience)
    frame = frame.rename(columns={'title': 'content'})
    ps = PorterStemmer()
    corpus = []
    frame = frame.reset_index(drop=True)
    # Preprocesamiento de textos
    for i in range(0, len(frame)):
        text = re.sub(r'http\S+', ' ', str(frame['content'][i]), flags=re.MULTILINE)
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = text.lower()
        text = text.split()
        text = [word for word in text if not word in stopwords.words('english')]
        text = ' '.join(text)
        corpus.append(text)
    frame['clean_content'] = corpus

    # 1-Creamos los Vectores ------------- importar sentence transformer para analisis sentimientos (pos/neg/neu), llamar sobre clean content

    

    def sentiment_analysis(content):
        """Devuelve análisis de sentimiento para una lista de textos."""
        analyzer = pipeline("sentiment-analysis", model="pysentimiento/robertuito-sentiment-analysis", device=0)
        results = analyzer(content)
        return results

    sentiment = sentiment_analysis(corpus)

    labels = [result['label'] for result in sentiment]
    counts = Counter(labels)


    model = SentenceTransformer(stmodel)
    embeddings = model.encode(frame['clean_content'], show_progress_bar=True)

    umap_embeddings = UMAP(n_neighbors=15,
                           n_components=5,
                           metric='cosine').fit_transform(embeddings)

    cluster = DBSCAN(min_samples=10).fit(umap_embeddings)

    docs_df = pd.DataFrame()
    docs_df['Doc'] = frame['clean_content']
    docs_df['Topic'] = cluster.labels_
    docs_df['Doc_ID'] = range(len(docs_df))
    docs_per_topic = docs_df.dropna(subset=['Doc']).groupby(['Topic'], as_index=False).agg({'Doc': ' '.join})

    

    def c_tf_idf(documents, m, ngram_range=(1, 1)):
        """Calcula c-TF-IDF para extracción de tópicos."""
        count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(documents)
        t = count.transform(documents).toarray()
        w = t.sum(axis=1)
        tf = np.divide(t.T, w)
        sum_t = t.sum(axis=0)
        idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
        tf_idf = np.multiply(tf, idf)

        return tf_idf, count

    tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(frame['clean_content']))

    def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=10):
        """Extrae las n palabras más relevantes por tópico."""
        words = count.get_feature_names_out()
        labels = list(docs_per_topic.Topic)
        tf_idf_transposed = tf_idf.T
        indices = tf_idf_transposed.argsort()[:, -n:]
        top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in
                       enumerate(labels)}
        return top_n_words


    top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=10)
    topicos = [top_n_words]


    # Formato de respuesta
    df_rows = []
    for topic, word_weight_list in top_n_words.items():
        words = ', '.join(word for word, _ in word_weight_list)
        df_rows.append({'Topic': topic, 'Words': words})

    response = pd.DataFrame(df_rows)

    final_response = {
        "topics": response.to_dict(orient="records"),
        "sentiment_counts": counts
    }

    return Response(json.dumps(final_response), media_type="application/json")


correlated_titles = pd.DataFrame()
topico_seleccionado = -2


@routeranalysis.get("/api/news")
async def related_news(n_topic: int = Query(..., title="Seleccione un tópico")): 
    global topicos

    if not topicos:  # Simplificar la validación
        return JSONResponse(
            content={"error": "Ejecuta primero una búsqueda"},
            status_code=400
        )

    topics = topicos[-1]

    if n_topic not in topics:
        return JSONResponse(
            content={"error": "Tópico no válido"},
            status_code=400
        )

    if n_topic > len(topics) - 2:

        return 'Please input a valid topic number'

    global topico_seleccionado
    topico_seleccionado = n_topic

    palabras = topics[n_topic]
    palabras = [tupla[0] for tupla in palabras]
    palabras_search = " OR ".join(palabras)
    

    newsapi = NewsApiClient(api_key='xxxxxx')



    data = newsapi.get_everything(q = palabras_search,
    language='en',
    sort_by='relevancy')

    if 'articles' not in data:
        return 'No recent news were found for the topic.'

    news = data['articles']
    df = pd.DataFrame(news)

    df = df.drop_duplicates(subset=['title'], keep='last')
    df.reset_index(drop=True, inplace=True)

    frame = df
    frame = frame.rename(columns={'title': 'description'})
    ps = PorterStemmer()
    corpus = []
    frame = frame.reset_index(drop=True)
    for _, row in frame.iterrows():
        text = re.sub(r'http\S+', ' ', str(row['description']), flags=re.MULTILINE)
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        text = text.lower()
        text = text.split()
        text = [word for word in text if word not in stopwords.words('english')]
        text = ' '.join(text)
        corpus.append(text)

    frame['clean_content'] = corpus
    url_index = frame.columns.get_loc("url")  # Encuentra el índice de "url"

    frame = frame.iloc[:, [1, 2, url_index, -1]]  # Mantiene 2 y añade "url"

    filas_sin_duplicados = frame.drop_duplicates(subset=['description'])
    frame = filas_sin_duplicados
    frame.reset_index(drop=True, inplace=True)

    # Convierte la lista de palabras en una cadena separada por espacios
    topic_words = " ".join(palabras).replace(", ", " ")

    topic_words = [topic_words]

    model = SentenceTransformer('all-mpnet-base-v2')

    # creamos los embeddings (creacion de la similitud)

    embeddings_title = model.encode(list(frame.clean_content))
    embedding_topic = model.encode(topic_words)


    def constructCorrelations(topic_embedding, embeddings, dataframe):
        correlations = pd.DataFrame(index=range(len(dataframe)), columns=['Correlation', 'Title', 'url'])
        for i in range(0, len(dataframe)):
            # obtenemos la similitud de todos los documentos
            array = cosine_similarity([embeddings[i]], topic_embedding)
            correlations.loc[i, 'Correlation'] = array[0]
            correlations.loc[i, 'Title'] = dataframe.loc[i, 'description']
            correlations.loc[i, 'url'] = dataframe.loc[i, 'url']
        return correlations

    global correlated_titles

    correlated_titles = constructCorrelations(embedding_topic, embeddings_title, frame)
    correlated_news = correlated_titles.sort_values(by='Correlation', ascending=False)
    correlated_news['Correlation'] = correlated_news['Correlation'].astype(float)

    correlated_titles = correlated_news.head(5)


    correlated_news = correlated_news[['Title', 'Correlation', 'url']]
# devolver a capa de presentacion las noticias más relacionadas
    return Response(correlated_news.to_json(orient="records"), media_type="application/json")


@routeranalysis.get("/api/explanation")
async def get_explanation():
    global topicos
    client = OpenAI(
        api_key = 'xxxxxx', #chatgpt3.5
    )
    
    global correlated_titles
    if correlated_titles.empty:

        return "In order to use this function, please execute the Related News function first."

    global topico_seleccionado
    n_topic = topico_seleccionado

    topics = topicos[0]
    palabras = topics[n_topic]
    palabras = [tupla[0] for tupla in palabras]
    palabras = ', '.join(palabras)


    titles_string = ', '.join(correlated_titles['Title'])

    prompt2 = '''Look at these words:''' + palabras + '''
They describe a certain recently relevant topic. These are some recent correlated news I've found to said topic:''' + titles_string +'''
I would like you to write an explanation about the latest trends and news surrounding these concepts. Do not just rewrite all of the words I gave you at the beggining. Lean more towards the news titles if possible'''
    

    prompt = ''' With a topic modelling algorithm I've obtained the following topic described by this top words: ''' + palabras + '''
                 And I want you to create an explanation about why that topic has emerged as a topic of interest making use of the following related news titles obtained: 
                 ''' + titles_string + '''

                 Basycally I want the explanation to be a explanation of what the topic is about and why has emerged as a topic of interest recently (DO NOT list the top topic words)'''

    
    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt2}]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )

        return response.choices[0].message.content.strip()
    response = get_completion(prompt2)

    return response

@routeranalysis.get("/api/fakenews")
async def get_fakenews(text: str):
    client = OpenAI(
        api_key = 'xxxxxx', #chatgpt3.5
    )
    from pathlib import Path
    import pickle

    BASE_DIR = Path(__file__).resolve().parent.parent  # Esto apunta a fastapi/
    MODEL_PATH = BASE_DIR / "model" / "model.pkl"
    VECTORIZER_PATH = BASE_DIR / "model" / "carecteristicas.pkl"

    import string
    from nltk.tokenize import word_tokenize
    from nltk.stem.wordnet import WordNetLemmatizer
    import pickle

    # Cargar modelo y vectorizador desde los archivos
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)

    wordnet = WordNetLemmatizer()
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    stopword_en = set(stopwords.words('english'))

    def normalize(s):
        replacements = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s

    def limpiar_texto(texto):
        tokens = word_tokenize(texto)
        tokens = [regex.sub('', t).lower() for t in tokens if t and t not in stopword_en]
        tokens = [normalize(wordnet.lemmatize(t)) for t in tokens if t]
        return ' '.join(tokens)
    
    clean_text = limpiar_texto(text)

    new_X = vectorizer.transform([clean_text])
    prediction = model.predict(new_X)[0]
    probability = model.predict_proba(new_X)[0][1]

    verdict = {0: "Real", 1: "Fake"}[prediction]
    probability = round(probability * 100, 2)

    prompt = '''I will provide you with a string of text representing an opinion found online in the shape of the title of an article or a forum comment. Your job is to provide an assesment of the chance of the message displayed being disinformation or not. You will do it by contrasting it with trusty online sources. You will respond with a short paragraph, and will reach a conclusion. The message is the following: ''' + text
    prompt2 = '''I will provide you with a string of text representing an opinion found online in the shape of the title of an article or a forum comment. It has been detected as  ''' + verdict +'''
     by a machine learning model that detects fake news. Your job is to  explain why that is the case. The message is the following: ''' + text

    def llm_assesment(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )

        return response.choices[0].message.content.strip()

    response = {
        "assessment": llm_assesment(prompt),
        "verdict": verdict,
        "probability": probability
    }

    return response



class AnalyzeRequest(BaseModel):
    paragraphs: List[str]

@routeranalysis.post("/api/analyze")
async def analyze(paragraphs: List[str], stmodel: str = "all-mpnet-base-v2"):
    global topicos

    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return JSONResponse(content={"error": "No paragraphs provided."}, status_code=400)
    
    N = len(paragraphs)

    ps = PorterStemmer()
    corpus = []

    def clean_text(text):
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = text.replace('\n', ' ')
        text = text.lower()
        text = ' '.join(text.split())
        return text
    
    for text in paragraphs:
        text = clean_text(text)  # <--- Limpiar texto
        if text:  # Filtrar textos vacíos
            corpus.append(text[:500])


    model = SentenceTransformer(stmodel)
    embeddings = model.encode(corpus, show_progress_bar=True)

    umap_embeddings = UMAP(n_neighbors=max(5,int(N/10)), n_components=5, metric='cosine').fit_transform(embeddings) #n_neighbors segun datos
    cluster = DBSCAN(min_samples=N//20).fit(umap_embeddings)

    
    docs_df = pd.DataFrame({"Doc": corpus, "Topic": cluster.labels_, "Doc_ID": range(len(corpus))})
    docs_per_topic = docs_df.groupby("Topic", as_index=False).agg({"Doc": ' '.join})
    
    def c_tf_idf(documents, m, ngram_range=(1, 1)):
        """Calcula c-TF-IDF para extracción de tópicos."""
        count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(documents)
        t = count.transform(documents).toarray()
        w = t.sum(axis=1)
        tf = np.divide(t.T, w)
        sum_t = t.sum(axis=0)
        idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
        return np.multiply(tf, idf), count
    
    tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, len(corpus))
    
    def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=10):
        """Extrae las n palabras más relevantes por tópico."""
        words = count.get_feature_names_out()
        labels = list(docs_per_topic.Topic)
        indices = tf_idf.T.argsort()[:, -n:]
        return {label: [(words[j], tf_idf.T[i][j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}
    
    top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=10)

    topicos=[top_n_words]
    
    sentiment_analyzer = pipeline("sentiment-analysis", 
                                  model="pysentimiento/robertuito-sentiment-analysis",
                                  device=0,
                                  truncation=True,
                                  max_length=512)
    sentiment_results = sentiment_analyzer(corpus)
    sentiment_counts = Counter([res['label'] for res in sentiment_results])
    
    response = {
        "topics": [{"Topic": topic, "Words": ', '.join([word for word, _ in words])} for topic, words in top_n_words.items()],
        "sentiment_counts": sentiment_counts
    }
    
    return JSONResponse(content=response)





