from celery import shared_task
from .models import WebhookResponse
from .utils import crear_registro_bd

@shared_task(name="procesar_pago_task")
def procesar_pago_task(webhook_response):
    print(f"[TASK] Procesando pago con transaction_id")
    print(f"[TASK] Actualizando Base de datos")
    response = WebhookResponse.model_validate(webhook_response)
    crear_registro_bd(response)
    print("[TASK] Llamar al servicio de notification_service")
    print("Pago realizado con exito")
    print("[TASK] Llamar al servicio de inventory_service")
    print("Inventario actualizado")