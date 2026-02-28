# ---------- Build base ----------
FROM python:3.13-slim AS base


WORKDIR /app

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# ---------- Runtime ----------
FROM base AS runtime

# (Opción A) Usando requirements.txt :
# COPY requirements*.txt /app/
# RUN pip install --upgrade pip \
#  && pip install -r requirements.txt -r requirements-dev.txt

# (Opción B):
COPY requirements.txt /app/
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

RUN pip install --upgrade pip \
    certifi \
    urllib3 \
    requests


# Copiamos solo el código de la app
COPY src /app/src

# Variables por defecto (puedes sobreescribir en runtime)
ENV ENVIRONMENT=test \
    PROJECT_ID=testproyectointegrador-488523 \
    TOPIC_ID=payments-service-queue \
    SUBSCRIPTION_ID=payments-service-queue-sub \
    DB_HOST=localhost \
    DB_PORT=5432 \
    DB_NAME=payment_service_db_test \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    INSTANCE_CONNECTION_NAME=testproyectointegrador-488523:us-central1:mi-postgres-instance


EXPOSE 8000

CMD ["python3", "-m", "src.run_worker"]