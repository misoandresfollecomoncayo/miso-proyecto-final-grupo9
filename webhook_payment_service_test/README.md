# payment_service — Servicio de Pagos (Experimentación)

Microservicio de experimentación encargado de gestionar los **pagos** que llegan del proveedor externo de pagos. Implementado con **Python 3.13 + FastAPI**, sin persistencia pero conectado a un tema Pub/Sub en GCP y empaquetado en **Docker**. Expone endpoints para poner un mensaje en un tema y para consultar el estado de salud del servicio.

## Índice

1. [Ejecución](#ejecución)
2. [Uso](#uso)
3. [Despliegue GCP](#despliegue-gcp)
4. [Autor](#autor)


## Ejecución

### A) Desarrollo local con pip
> Ejecutar **dentro de `webhook_payment_service_test/`** para levantar aplicación.

```bash
#Descarga de dependencias 
pip install -r requirements.txt
#Poner en funcionamiento en puerto 8000
python3 src/main.py
```

**Variables de entorno (ya definidas en compose):**

| Variable        | Default                          | Descripción |
|----------------|----------------------------------|------------|
| `API_HOST`     | `0.0.0.0`                        | Dirección en la que la API escucha conexiones entrantes (bind address). |
| `API_PORT`     | `8000`                           | Puerto en el que se expone la API. |
| `PROJECT_ID`   | `testproyectointegrador-488523`  | ID del proyecto en Google Cloud donde se encuentran los recursos. |
| `TOPIC_ID`     | `payments-service-queue`         | Nombre del tópico de Pub/Sub utilizado para publicar o consumir mensajes. |
| `ENVIRONMENT`  | `test`                           | Entorno de ejecución de la aplicación (`dev`, `test`, `prod`, etc.). |

## Uso

Este servicio expone endpoints para poner un mensaje en un tema Pub/Sub. A continuación se muestran ejemplos de consumo utilizando **cURL**.

```bash
# 1. Verificar estado del servicio (ping)
curl -X GET http://localhost:8000/health
# Respuesta: "200"

# 2. Consultar cantidad de trayectos
curl -X POST http://localhost:8000//webhook \
  -H "Content-Type: application/json" \
  -d '{
    "id_transaction":"test",
    "code": 200,
    "status": "ok"
}'
# Respuesta: {"id_transaction": "test", "code": 200, "status": "ok", "created_at": "2026-02-28T15:14:05.475710+00:00"}
```

## Despliegue GCP 

### Requisitos Previos en GCP

Antes del despliegue, debes:

1. Tener creado el proyecto en Google Cloud Platform.
2. Tener configurado Pub/Sub con el tópico correspondiente.
3. Tener creado un repositorio en Artifact Registry
4. Verificar que el `PROJECT_ID` y el `TOPIC_ID` coincidan con los creados en GCP.
5. Modificar las variables de entorno en el `Dockerfile`:

```dockerfile
ENV API_HOST=0.0.0.0 \
    API_PORT=8000 \
    PROJECT_ID=<tu-project-id> \
    TOPIC_ID=<tu-topic-id> \
    ENVIRONMENT=test
```
### Build de docker y publicación en registry

---
#### Build de la Imagen (Arquitectura Cloud Run)
```
docker buildx build --platform linux/amd64 -t my-service-webhook:latest .
```
---

---
#### Tag de la Imagen para Artifact Registry
```
docker tag my-service-webhook:latest <location-name>-docker.pkg.dev/<project-id>/<repository-name>/my-service-webhook:latest
```
---

---
#### Push a Artifact Registry
```
docker push <location-name>-docker.pkg.dev/<project-id>/<repository-name>/my-service-webhook:latest
```
---

---
#### Ejemplo:
```
docker push us-central1-docker.pkg.dev/testproyectointegrador-488523/webhookrepository/my-service-webhook:latest
```
---

### Despliegue en Cloud Run

Una vez subida la imagen:

1. Ir a **Cloud Run** en la consola de GCP.
2. Crear un grupo de trabajadores.
3. Seleccionar la imagen desde **Artifact Registry**.
4. Configurar:
   - **Región** (ej. `us-central1`)
   - **Variables de entorno** necesarias
   - **Permisos de IAM** (si usa Pub/Sub)
5. Desplegar el servicio.


## Autor

- Pablo Jose Rivera
- Contacto: `<p.riverah@uniandes.edu.co>`