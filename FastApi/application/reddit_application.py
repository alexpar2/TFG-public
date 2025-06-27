from persistence.reddit_persistence import *
from models.reddit import *
import json
from config.connection import conreddit, cancel_event
from fastapi import HTTPException
import prawcore
from .comun_application import ThreadWithReturnValue #clase hebra con retorno de valor

def get_reddit_default():
    """
    Obtiene las 10 publicaciones principales del subreddit 'python'.

    Returns:
        Lista de publicaciones con título e ID.
    """
    try:
        subreddit = conreddit.subreddit("python")
        subreddit._fetch()  # Verificación de existencia del subreddit
        top_posts = [{"Title": post.title, "ID": post.id} for post in subreddit.top(limit=10)]
        result = list(top_posts)
        if not result:
            raise HTTPException(status_code=404, detail="No posts found in the subreddit.")
        serializables = json.loads(json.dumps(result, default=str))
        return serializables
    except prawcore.exceptions.Redirect:
        raise HTTPException(status_code=404, detail="Subreddit not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Reddit: {str(e)}")

def get_all_reddits():
    """
    Obtiene todos los registros de Reddit de la base de datos.

    Returns:
        Lista de registros de Reddit.
    """
    try:
        myCursor = get_all_redditsDB()
        result = list(myCursor)
        if not result:
            raise HTTPException(status_code=404, detail="No Reddit records found in the database.")
        serializables = json.loads(json.dumps(result, default=str))
        return serializables
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from database: {str(e)}")

def insert_reddits(name: str):
    """
    Inserta las 5 publicaciones principales de un subreddit en la base de datos.

    Args:
        name: Nombre del subreddit.
    """
    try:
        subreddit = conreddit.subreddit(name)
        subreddit._fetch()  # Verificación de existencia del subreddit
        top_posts = subreddit.top(limit=5)
        reddit_posts = []  # Crear una lista vacía
        for post in top_posts:
            redditor_name = str(post.author)
            redditor = conreddit.redditor(redditor_name)
            if hasattr(redditor, 'comment_karma'):
                post_karma = str(redditor.comment_karma)
            else:
                post_karma = None
            reddit_post = Reddit(Title=post.title, ID=post.id, Author=redditor_name, URL=post.url, Score=post.score, Karma=post_karma)
            reddit_posts.append(reddit_post)
        if not reddit_posts:
            raise HTTPException(status_code=404, detail="No posts found to insert into the database.")
        insert_reddictsDB(reddit_posts)
    except prawcore.exceptions.Redirect:
        raise HTTPException(status_code=404, detail="Subreddit not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting data into database: {str(e)}")

def insert_reddits_coment(tema: str, publicaciones: int, profundidad: int, bajada: int, insertar: bool):
    """
    Inserta o visualiza comentarios de publicaciones de un subreddit en la base de datos.

    Args:
        tema: Nombre del subreddit.
        publicaciones: Número de publicaciones a recuperar.
        profundidad: Profundidad máxima de comentarios.
        bajada: Número máximo de niveles de comentarios.
        insertar: Booleano para determinar si se insertan los datos en la base de datos.
    """
    global cancel_event

    # Resetear el evento de cancelación
    cancel_event.clear()

    def run_insertion():
        try:
            nombre_subreddit = tema
            limite_publicaciones = publicaciones
            max_profundidad = profundidad
            limite_bajada = bajada
            comentarios_reddit = obtener_comentarios_reddit(nombre_subreddit, limite_publicaciones, max_profundidad, limite_bajada)
            
            if not comentarios_reddit:
                raise HTTPException(status_code=404, detail="No comments found for the given subreddit.")
            
            posts = []
            for publicacion in comentarios_reddit:
                if cancel_event.is_set():
                    raise Exception("Proceso cancelado")

                post = RedditPost(
                    Title=publicacion["título"],
                    ID=publicacion["ID"],
                    Author=publicacion["Author"],
                    URL=publicacion["URL"],
                    Score=publicacion["Score"],
                    Karma=publicacion["Karma"],
                    Comments=[]
                )
                for comentario in publicacion["comentarios"]:
                    if cancel_event.is_set():
                        raise Exception("Proceso cancelado")

                    comment = procesar_comentario(comentario)
                    post.Comments.append(comment)
                posts.append(post)
            
            if insertar:
                if cancel_event.is_set():
                    raise Exception("Proceso cancelado")
                insert_reddicts2DB(posts)
            else:
                return posts

            return posts

        except prawcore.exceptions.Redirect:
            raise HTTPException(status_code=404, detail="Subreddit not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inserting comments into database: {str(e)}")

    # Ejecutar el proceso de inserción en un hilo separado y obtener el resultado
    insertion_thread = ThreadWithReturnValue(target=run_insertion)
    insertion_thread.start()
    result = insertion_thread.join()

    # Verificar si la inserción fue cancelada
    if cancel_event.is_set():
        raise HTTPException(status_code=400, detail="Proceso cancelado")

    # Devolver el resultado almacenado
    return result

def procesar_comentario(comentario_data):
    """
    Procesa un comentario y sus respuestas de manera recursiva.

    Args:
        comentario_data: Diccionario con los datos del comentario.

    Returns:
        Objeto RedditComment con los datos del comentario y sus respuestas.
    """
    try:
        if cancel_event.is_set():
            raise Exception("Proceso cancelado")
        
        if not isinstance(comentario_data, dict):
            return None  # Retorna None si no es un diccionario

        # Procesa el comentario actual
        comment = RedditComment(
            Body=comentario_data.get("cuerpo", ""),  # Usa get() para evitar KeyError
            Author=comentario_data.get("autor", "")
        )
        
        # Procesa las respuestas recursivamente
        if "respuestas" in comentario_data:
            for respuesta in comentario_data["respuestas"]:
                if cancel_event.is_set():
                    raise Exception("Proceso cancelado")

                reply = procesar_comentario(respuesta)
                if reply:  # Agrega la respuesta solo si no es None
                    comment.Replies.append(reply)
        
        return comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing comment: {str(e)}")



def obtener_comentarios_recursivos(comentario, profundidad, max_profundidad, limite_bajada):
    """
    Obtiene recursivamente los comentarios y sus respuestas hasta una profundidad especificada.

    Args:
        comentario: Objeto de comentario PRAW
        profundidad: Profundidad actual
        max_profundidad: Profundidad máxima a explorar
        limite_bajada : Cuantos comentarios lee en ese nodo
    Returns:
        Lista de datos de comentarios (cuerpo, autor, respuestas)
    """
    if cancel_event.is_set():
        raise Exception("Proceso cancelado")

    if profundidad > max_profundidad:
        return []

    datos_comentario = {
        "cuerpo": comentario.body,
        "autor": comentario.author.name,
        "respuestas": []
    }
    if profundidad != max_profundidad:
        for respuesta in comentario.replies[:limite_bajada]:
            if cancel_event.is_set():
                raise Exception("Proceso cancelado")

            if respuesta.author:
                datos_respuesta = {
                    "cuerpo": respuesta.body,
                    "autor": respuesta.author.name,
                    "respuestas": obtener_comentarios_recursivos(respuesta, profundidad + 1, max_profundidad, limite_bajada)
                }
                datos_comentario["respuestas"].append(datos_respuesta)

    return datos_comentario


def obtener_comentarios_reddit(subreddit_nombre, limite_publicaciones=1, max_profundidad=3, limite_bajada=3):
    """
    Obtiene comentarios de una publicación de subreddit y sus respuestas.

    Args:
        subreddit_nombre: Nombre del subreddit
        limite_publicaciones: Número de publicaciones principales a recuperar
        max_profundidad: Profundidad máxima a explorar para comentarios
        limite_bajada : Cuantos comentarios baja en el nodo

    Returns:
        Lista de datos de publicaciones (título, URL, comentarios)
    """
    try:
        if cancel_event.is_set():
            raise Exception("Proceso cancelado")

        subreddit = conreddit.subreddit(subreddit_nombre)
        subreddit._fetch()  # Verificación de existencia del subreddit
        datos_publicaciones = []

        for publicacion in subreddit.top(limit=limite_publicaciones):
            if cancel_event.is_set():
                raise Exception("Proceso cancelado")

            redditor_name = str(publicacion.author)
            redditor = conreddit.redditor(redditor_name)
            if hasattr(redditor, 'comment_karma'):
                post_karma = str(redditor.comment_karma)
            else:
                post_karma = '0'

            datos_publicacion = {
                "título": publicacion.title,
                "Author": redditor_name,
                "URL": publicacion.url,
                "ID": publicacion.id,
                "Score": publicacion.score,
                "Karma": post_karma,
                "comentarios": []
            }

            publicacion.comments.replace_more(limit=5) #aquí falla
            for comentario in publicacion.comments.list()[:limite_bajada]:
                if cancel_event.is_set():
                    raise Exception("Proceso cancelado")

                if comentario.author:
                    datos_comentario = obtener_comentarios_recursivos(comentario, profundidad=1, max_profundidad=max_profundidad, limite_bajada=limite_bajada)
                    datos_publicacion["comentarios"].append(datos_comentario)

            datos_publicaciones.append(datos_publicacion)

        if not datos_publicaciones:
            raise HTTPException(status_code=404, detail="No posts found in the subreddit.")
        
        return datos_publicaciones
    except prawcore.exceptions.Redirect:
        raise HTTPException(status_code=404, detail="Subreddit not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching comments from Reddit: {str(e)}")



