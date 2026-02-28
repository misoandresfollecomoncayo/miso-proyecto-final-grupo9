import json
import threading
from google.cloud import pubsub_v1
from .tasks import procesar_pago_task
from .config import PROJECT_ID, SUBSCRIPTION_ID

def start_pubsub_consumer():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    def callback(message):
        try:
            payload = json.loads(message.data.decode("utf-8"))
            procesar_pago_task.delay(payload)
            message.ack()
        except Exception as e:
            print("Error procesando mensaje:", e)
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Worker listo: escuchando la suscripción de Pub/Sub...")

    try:
        streaming_pull_future.result()  # Bloquea el hilo principal
    except KeyboardInterrupt:
        streaming_pull_future.cancel()