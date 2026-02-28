from celery import Celery
from celery.signals import worker_ready
from threading import Thread
from .subscriber import start_pubsub_consumer
from .config import PROJECT_ID

celery_app = Celery(
    "worker",
    broker="memory://", 
    backend="rpc://"   
)

celery_app.conf.task_routes = {
    "tasks.procesar_pago_task": {"queue": "payments_queue"}
}