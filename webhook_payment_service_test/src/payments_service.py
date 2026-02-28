from fastapi import FastAPI, Request, HTTPException
from main import TOPIC_ID, PROJECT_ID
from models import WebhookResponse
from json import loads, JSONDecodeError, dumps
from datetime import datetime, timezone
from google.cloud import pubsub_v1

app = FastAPI()
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.post("/webhook")
async def payment_webhook(request: Request):
    created_at = datetime.now(timezone.utc).isoformat()
    body = await request.body()
    try:
        data = loads(body) if body else {}
    except JSONDecodeError:
        data = {}
    
    try:
        payload = WebhookResponse.model_validate(data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    payload.created_at = created_at

    #Convertir el mensaje en bytes
    message_bytes = dumps(payload.model_dump()).encode("utf-8")

    future = publisher.publish(topic_path, message_bytes)

    print(f"Mensaje enviado: {future.result()}")

    return payload

@app.get("/health")
async def health_check():
    return 200