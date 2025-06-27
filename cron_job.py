import requests
from datetime import datetime, timedelta

def log_message(message):
    #Función para registrar mensajes en un archivo de log.
    with open("cron_job_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

try:
    # Calcular la fecha de ayer
    fecha_ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # URL de la API
    url = f"http://127.0.0.1:8000/api/googlenews/insertSecure/Pyhton?fecha_ini={fecha_ayer}&fecha_hasta={fecha_ayer}&cantidad_webs_seguras=45"

    # Hacer la llamada PUT a la API
    response = requests.put(url)

    # Verificar la respuesta
    if response.status_code == 200:
        log_message("Datos insertados correctamente")
    else:
        log_message(f"Error al insertar datos: {response.status_code} - {response.text}")

except requests.exceptions.ConnectionError as e:
    log_message(f"ConnectionError: No se puede establecer una conexión con el servidor - {str(e)}")
except Exception as e:
    log_message(f"Exception: Ocurrió un error - {str(e)}")
