from persistence.googlenews_persistence import *
from models.googlenews import *
import json
from config.connection import apikeygnews, google_news, cancel_event

import urllib.request
from datetime import datetime
import threading
from .comun_application import ThreadWithReturnValue  


# def get_all_products():

#    myCursor = get_all_productsDB()
#    result = list(myCursor)
#    serializables = json.loads(json.dumps(result, default=str))
#    return serializables
def get_all_gnews():

   myCursor = get_all_gnewsDB()
   result = list(myCursor)
   serializables = json.loads(json.dumps(result, default=str))
   return serializables
   

#Solo muestra los datos de manera generia no inserta en base de datos


def get_gnews_default():
   category = "general"
   url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=5&apikey={apikeygnews}"

   with urllib.request.urlopen(url) as response:
      data = json.loads(response.read().decode("utf-8"))
      articles = data["articles"]
      # Crear una lista para almacenar los títulos limpios
      all_articles = []

      
# Iterar sobre cada artículo en la lista 'articles'
      for article in articles:
         # Extraer el título y el contenido limpio (sin la muletilla)
         title = article['title']
         name = article['source']['name']
         clean_content = article['content'].split(' [')[0]
         url = article['url']
         
         # Crear un diccionario con los campos 'title' y 'content'
         article_dict = {'title': title,'name': name, 'content': clean_content, 'url': url}
         
         # Agregar el diccionario a la lista 'all_articles'
         all_articles.append(article_dict) 
#    myCursor = get_all_pruebasDB()
   result = list(all_articles)
   serializables = json.loads(json.dumps(result, default=str))
   return serializables


# Insertar una busqueda por tema 
def insert_gnewsSinL(name:str):   

   url = f"https://gnews.io/api/v4/search?q={name}&lang=en&country=us&max=10&apikey={apikeygnews}"

   with urllib.request.urlopen(url) as response:
      data = json.loads(response.read().decode("utf-8"))
      articles = data["articles"]
      # Crear una lista para almacenar los títulos limpios
      all_articles = []

      
# Iterar sobre cada artículo en la lista 'articles'
   for article in articles:
      # Extraer el título y el contenido limpio (sin la muletilla)
      title = article['title']
      name = article['source']['name']
      clean_content = article['content'].split(' [')[0]
      url = article['url']
      
      # Crear un diccionario con los campos 'title' y 'content'
      article_dict = GNew(Title= title,MediaName= name, content= clean_content, url= url)
      
      # Agregar el diccionario a la lista 'all_articles'
      all_articles.append(article_dict)

   insert_gnewsDB(all_articles)




def insert_gnews(tema: str, insert: bool):
    """
    Inserta o visualiza noticias basadas en una búsqueda por tema en la base de datos.

    Args:
        tema: Término de búsqueda.
        insert: Booleano para determinar si se insertan los datos en la base de datos.
    """
    global cancel_event

    # Resetear el evento de cancelación
    cancel_event.clear()

    def run_insertion():
        news = google_news.get_news(tema)

        if not news:
            raise HTTPException(status_code=404, detail="Tema no encontrado")

        all_news = []
        for new in news:
            if cancel_event.is_set():
                raise Exception("Proceso cancelado")

            title = new['title']
            name = new['publisher']['title']
            clean_content = ""
            url = new['url']

            # Obtener el contenido
            article = google_news.get_full_article(url)
            if article is not None:
                clean_content = article.text

            # Crear un diccionario de Gnew
            article_dict = GNew(Title=title, MediaName=name, content=clean_content, url=url)

            # Agregar el diccionario a la lista 'all_news'
            all_news.append(article_dict)

        if insert:
            if cancel_event.is_set():
                raise Exception("Proceso cancelado")
            insert_gnewsDB(all_news)
        else:
            return all_news

        return all_news

    # Ejecutar el proceso de inserción en un hilo separado y obtener el resultado
    insertion_thread = ThreadWithReturnValue(target=run_insertion)
    insertion_thread.start()
    result = insertion_thread.join()

    # Verificar si la inserción fue cancelada
    if cancel_event.is_set():
        raise HTTPException(status_code=400, detail="Proceso cancelado")

    return result



# Insertar una busqueda por tema y fecha
def insert_gnewsF(tema:str, fecha_ini : str,fecha_hasta : str ):   
 

   # fecha_inicio = datetime.strptime(fecha_ini, "%Y-%m-%d")
   # fecha_fin  = datetime.strptime(fecha_hasta, "%Y-%m-%d")

   google_news.start_date = (fecha_ini.year, fecha_ini.month, fecha_ini.day) 
   google_news.end_date = (fecha_hasta.year, fecha_hasta.month, fecha_hasta.day) 

   news = google_news.get_news(tema)

   if not news:
      return "Tema no encontrado"
   else: 

      all_news = []   
   # Iterar sobre cada artículo en la lista 'news'
      for new in news:
         #extraccion de datos
         title = new['title']
         name = new['publisher']['title']
         clean_content = ""
         url = new['url']

         
         #Obtenemos el contenido
         article = google_news.get_full_article(url)
         if article is not None:
            clean_content = article.text
         
         # Crear un diccionario de Gnew
         article_dict = GNew(Title= title,MediaName= name, content= clean_content, url= url)
         
         # Agregar el diccionario a la lista 'all_articles'
         all_news.append(article_dict)

      insert_gnewsDB(all_news)


def obtener_url_id(id:ObjectId):   
   #obtenemos la url
   return obtener_url_por_id(id)





#Obentener el contenido de un post concreto
def obtener_contenido_id(id:ObjectId):   
   #obtenemos la url
   url = obtener_url_por_id(id)
   #Obtenemos el contenido
   article = google_news.get_full_article(url)
   if article is not None:
      content = article.text
       #actualizamos
      update_content_in_gnewsDB(id, content)
   else : 
      return f"Contenido no disponible"
  
   


list_of_trusted_sources = ["nytimes.com",
"wsj.com",
"bbc.com",
"economist.com",
"newyorker.com",
"ap.org",
"reuters.com",
"bloomberg.com",
"foreignaffairs.com",
"theatlantic.com",
"politico.com",
"c-span.org",
"csmonitor.com",
"npr.org",
"propublica.org",
"eu.usatoday.com",
"fair.org",
"pewresearch.org",
"pbs.org",
"cbsnews.com",
"theguardian.com",
"edition.cnn.com",
"nbcnews.com",
"forbes.com",
"theconversation.com",
"upi.com",
"journalistsresource.org",
"snopes.com",
"huffpost.com",
"foxnews.com",
"dailymail.co.uk",
"factcheck.org",
"politifact.com",
"avclub.com",
"bandcamp.com",
"deadline.com",
"heavy.com",
"indiewire.com",
"pitchfork.com",
"rollingstone.com",
"upworthy.com",
"variety.com",
"vibe.com",
"vulture.com",
"washingtonpost.com"]



from datetime import timedelta, datetime
from gnews import GNews
from tqdm import tqdm
   


# Insertar una busqueda por tema y fecha
def insert_gnewsSecure( fecha_ini : str,fecha_hasta : str ):   
 
    fecha_inicio = datetime.strptime(fecha_ini, "%Y-%m-%d")
    fecha_fin = datetime.strptime(fecha_hasta, "%Y-%m-%d")
    results = []

    for source in list_of_trusted_sources[:2]:
        start_date = fecha_inicio
        end_date = fecha_fin
        start_date_plus_one = start_date + timedelta(days=5)

        pbar = tqdm(total=(fecha_fin - fecha_inicio).days)

        while start_date < end_date:
            try:
                google_news = GNews(language='en', start_date=(start_date.year, start_date.month, start_date.day), end_date=(start_date_plus_one.year, start_date_plus_one.month, start_date_plus_one.day), max_results=100)
                results_act = google_news.get_news_by_site(source)
                results.append(results_act)

            except Exception as e:
                print(f"Error occurred while fetching news for {source}:", e)

            start_date += timedelta(days=5)
            start_date_plus_one += timedelta(days=5)

            pbar.update(5)

    concatenated_list = [item for sublist in results for item in sublist]


    all_news = []   
# Iterar sobre cada artículo en la lista 'news'
    for new in concatenated_list:
      #extraccion de datos
      title = new['title']
      name = new['publisher']['title']
      clean_content = "" 
      url = new['url']

      #Obtenemos el contenido
      article = google_news.get_full_article(url)
      if article is not None:
         clean_content = article.text
      
      # Crear un diccionario de Gnew
      article_dict = GNew(Title= title,MediaName= name, content= clean_content, url= url)
      
      # Agregar el diccionario a la lista 'all_articles'
      all_news.append(article_dict)


    insert_gnewsDB(all_news)


def insert_gnewsSecureCantidad(fecha_ini: str, fecha_hasta: str, cantidad: int):
    """
    Inserta noticias de una lista de fuentes confiables en un rango de fechas en la base de datos.

    Args:
        fecha_ini: Fecha de inicio (YYYY-MM-DD).
        fecha_hasta: Fecha de fin (YYYY-MM-DD).
        cantidad: Cantidad de fuentes confiables a utilizar.

    Returns:
        Lista de fuentes sin contenido.
    """
    global cancel_event

    # Resetear el evento de cancelación
    cancel_event.clear()

    def run_insertion():
        results = []
        fuentes_sin_contenido = []

        for source in list_of_trusted_sources[:cantidad]:
            if cancel_event.is_set():
                raise Exception("Proceso cancelado")

            start_date = fecha_ini
            end_date = fecha_hasta
            noticia_diaria = (start_date == end_date)
            start_date_plus_one = start_date + timedelta(days=5)

            pbar = tqdm(total=(fecha_hasta - fecha_ini).days)

            while start_date < end_date or noticia_diaria:
                try:
                    if cancel_event.is_set():
                        raise Exception("Proceso cancelado")

                    google_news = GNews(language='en', start_date=(start_date.year, start_date.month, start_date.day), end_date=(start_date_plus_one.year, start_date_plus_one.month, start_date_plus_one.day), max_results=100)
                    results_act = google_news.get_news_by_site(source)
                    results.append(results_act)

                except Exception as e:
                    print(f"Error occurred while fetching news for {source}:", e)

                start_date += timedelta(days=5)
                start_date_plus_one += timedelta(days=5)
                noticia_diaria = False
                pbar.update(5)

        concatenated_list = [item for sublist in results for item in sublist]

        all_news = []
        for new in concatenated_list:
            if cancel_event.is_set():
                raise Exception("Proceso cancelado")

            title = new['title']
            name = new['publisher']['title']
            clean_content = ""
            url = new['url']

            article = google_news.get_full_article(url)
            if article is not None:
                clean_content = article.text
            else:
                fuentes_sin_contenido.append(name)

            article_dict = GNew(Title=title, MediaName=name, content=clean_content, url=url)
            all_news.append(article_dict)

        if not all_news:
            raise HTTPException(status_code=400, detail="No news articles to insert into the database.")

        insert_gnewsDB(all_news)

        return fuentes_sin_contenido

    # Ejecutar el proceso de inserción en un hilo separado y obtener el resultado
    insertion_thread = ThreadWithReturnValue(target=run_insertion)
    insertion_thread.start()
    result = insertion_thread.join()

    # Verificar si la inserción fue cancelada
    if cancel_event.is_set():
        raise HTTPException(status_code=400, detail="Proceso cancelado")

    return result

def insert_gnews_custom_sources(fecha_ini: str, fecha_hasta: str, sources: list):
    """
    Inserta noticias de una lista personalizada de fuentes confiables en un rango de fechas en la base de datos.

    Args:
        fecha_ini: Fecha de inicio (YYYY-MM-DD).
        fecha_hasta: Fecha de fin (YYYY-MM-DD).
        sources: Lista de fuentes confiables a utilizar.

    Returns:
        Lista de fuentes sin contenido.
    """
    global cancel_event

    # Resetear el evento de cancelación
    cancel_event.clear()

    def run_insertion():
        try:
            results = []
            fuentes_sin_contenido = []

            for source in sources:
                if cancel_event.is_set():
                    raise Exception("Proceso cancelado")

                start_date = fecha_ini
                end_date = fecha_hasta
                noticia_diaria = (start_date == end_date)
                start_date_plus_one = start_date + timedelta(days=5)

                pbar = tqdm(total=(end_date - start_date).days)

                while start_date < end_date or noticia_diaria:
                    try:
                        if cancel_event.is_set():
                            raise Exception("Proceso cancelado")

                        google_news = GNews(language='en', start_date=(start_date.year, start_date.month, start_date.day), end_date=(start_date_plus_one.year, start_date_plus_one.month, start_date_plus_one.day), max_results=100)
                        results_act = google_news.get_news_by_site(source)
                        if results_act:
                            results.append(results_act)
                    except Exception as e:
                        print(f"Error occurred while fetching news for {source}:", e)

                    start_date += timedelta(days=5)
                    start_date_plus_one += timedelta(days=5)
                    noticia_diaria = False
                    pbar.update(5)

            concatenated_list = [item for sublist in results for item in sublist]

            if not concatenated_list:
                raise HTTPException(status_code=400, detail="No news articles found for the given sources and date range.")

            all_news = []
            for new in concatenated_list:
                if cancel_event.is_set():
                    raise Exception("Proceso cancelado")

                title = new['title']
                name = new['publisher']['title']
                clean_content = ""
                url = new['url']
                article = google_news.get_full_article(url)
                if article is not None:
                    clean_content = article.text
                else:
                    fuentes_sin_contenido.append(name)
                article_dict = GNew(Title=title, MediaName=name, content=clean_content, url=url)
                all_news.append(article_dict)

            if not all_news:
                raise HTTPException(status_code=400, detail="No news articles to insert into the database.")

            insert_gnewsDB(all_news)
            return fuentes_sin_contenido
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

    # Ejecutar el proceso de inserción en un hilo separado y obtener el resultado
    insertion_thread = ThreadWithReturnValue(target=run_insertion)
    insertion_thread.start()
    result = insertion_thread.join()

    # Verificar si la inserción fue cancelada
    if cancel_event.is_set():
        raise HTTPException(status_code=400, detail="Proceso cancelado")

    return result

