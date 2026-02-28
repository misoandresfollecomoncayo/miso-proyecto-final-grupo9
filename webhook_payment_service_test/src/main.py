from os import getenv, environ

import uvicorn

API_HOST = getenv("SIDECAR_HOST", "0.0.0.0")
API_PORT = getenv("SIDECAR_PORT", "8000")
PROJECT_ID = getenv("PROJECT_ID","testproyectointegrador-488523")
TOPIC_ID = getenv("TOPIC_ID", "payments-service-queue")
ENVIRONMENT = getenv("ENVIRONMENT", "test")

if ENVIRONMENT == "dev":
    environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./apikey.json"


if __name__ == "__main__":
    uvicorn.run("payments_service:app", host=API_HOST, port=int(API_PORT))
