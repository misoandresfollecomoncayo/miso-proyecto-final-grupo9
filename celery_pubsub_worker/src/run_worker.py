import threading
from .celery_app import celery_app
from .subscriber import start_pubsub_consumer
from.config import ENVIRONMENT
from os import environ

if ENVIRONMENT == "dev":
    environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./apikey.json"

# Arranca el consumer en un hilo separado
thread = threading.Thread(target=start_pubsub_consumer, daemon=True)
thread.start()

# Arranca Celery worker (para procesar las tareas que se disparan desde Pub/Sub)
celery_app.worker_main([
    "worker",
    "--concurrency=4",
    "--pool=threads", 
    "--loglevel=info"
    ])