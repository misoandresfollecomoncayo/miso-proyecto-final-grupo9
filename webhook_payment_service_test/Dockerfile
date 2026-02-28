# ---------- Build base ----------
FROM python:3.13-slim AS base


WORKDIR /app

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

# Copiamos solo el código de la app
COPY src /app/src

# Variables por defecto (puedes sobreescribir en runtime)
ENV API_HOST=0.0.0.0 \
    API_PORT=8000 \
    PROJECT_ID=testproyectointegrador-488523 \
    TOPIC_ID=payments-service-queue \
    ENVIRONMENT=test

EXPOSE 8000

CMD ["python3", "src/main.py"]