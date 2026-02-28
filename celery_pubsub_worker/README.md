# payment_service_worker — Servicio Worker de Pagos (Experimentación)

Microservicio de experimentación encargado de gestionar los **pagos** que llegan del proveedor externo de pagos. Implementado con **Python 3.13 + Celery**, Con persistencia a una base de datos de Cloud SQL (GCP) y escuchando los mensajes de una subscripción Pub/Sub en GCP y empaquetado en **Docker**. Escucha los mensajes y lo registra en una base de datos.

## Índice

1. [Ejecución](#Ejecución)
2. [Despliegue GCP](#despliegue-gcp)
3. [Autor](#autor)


## Ejecución

### A) Desarrollo local con pip
> Ejecutar **dentro de `celery_pubsub_worker/`** para levantar aplicación.

```bash
#Descarga de dependencias 
pip install -r requirements.txt
#Poner en funcionamiento en puerto 8000
python3 python3 -m src.run_worker
```

**Variables de entorno (ya definidas en compose):**

| Variable                     | Default                                                         | Descripción |
|------------------------------|-----------------------------------------------------------------|------------|
| `ENVIRONMENT`                | `test`                                                          | Entorno de ejecución de la aplicación (`dev`, `test`, `prod`, etc.). |
| `PROJECT_ID`                 | `testproyectointegrador-488523`                                 | ID del proyecto en Google Cloud donde se encuentran los recursos. |
| `TOPIC_ID`                   | `payments-service-queue`                                        | Nombre del tópico de Pub/Sub utilizado para publicar mensajes. |
| `SUBSCRIPTION_ID`            | `payments-service-queue-sub`                                    | Nombre de la suscripción asociada al tópico de Pub/Sub para consumo de mensajes. |
| `DB_HOST`                    | `localhost`                                                     | Host de la base de datos PostgreSQL. |
| `DB_PORT`                    | `5432`                                                          | Puerto de conexión a PostgreSQL (requerido fijo para Cloud SQL). |
| `DB_NAME`                    | `payment_service_db_test`                                       | Nombre de la base de datos. |
| `DB_USER`                    | `postgres`                                                      | Usuario de conexión a la base de datos. |
| `DB_PASSWORD`                | `postgres`                                                      | Contraseña del usuario de la base de datos. |
| `INSTANCE_CONNECTION_NAME`   | `testproyectointegrador-488523:us-central1:mi-postgres-instance` | Nombre de conexión de la instancia de Cloud SQL (formato: `project:region:instance`). |

## Despliegue GCP 

### Requisitos Previos en GCP

Antes del despliegue, debes:

1. Tener creado el proyecto en Google Cloud Platform.
2. Tener configurado Pub/Sub con el tópico correspondiente.
3. Tener creado una Base de datos en Cloud SQL (GCP) o localmente (para `ENVIRONMENT`=`DEV`)
3. Tener creado un repositorio en Artifact Registry
4. Modificar las variables de entorno en el `Dockerfile`:

```dockerfile
ENV ENVIRONMENT=prod \
    PROJECT_ID=<your-gcp-project-id> \
    TOPIC_ID=<your-pubsub-topic-id> \
    SUBSCRIPTION_ID=<your-pubsub-subscription-id> \
    DB_HOST=localhost \
    DB_PORT=5432 \
    DB_NAME=payment_service_db_test \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    INSTANCE_CONNECTION_NAME=<your-project-id>:<region>:<cloud-sql-instance-name>
```
### Build de docker y publicación en registry

---
#### Build de la Imagen (Arquitectura Cloud Run)
```
docker buildx build --platform linux/amd64 -t my-service:latest .
```
---

---
#### Tag de la Imagen para Artifact Registry
```
docker tag my-service:latest <location-name>-docker.pkg.dev/<project-id>/<repository-name>/my-service:latest
```
---

---
#### Push a Artifact Registry
```
docker push <location-name>-docker.pkg.dev/<project-id>/<repository-name>/my-service:latest
```
---

---
#### Ejemplo:
```
docker push us-central1-docker.pkg.dev/testproyectointegrador-488523/webhookrepository/my-service:latest
```
---

### Despliegue en Cloud Run

Una vez subida la imagen:

1. Ir a **Cloud Run** en la consola de GCP.
2. Crear un servicio.
3. Seleccionar la imagen desde **Artifact Registry**.
4. Configurar:
   - **Región** (ej. `us-central1`)
   - **Variables de entorno** necesarias
   - **Permisos de IAM** (si usa Pub/Sub)
5. Desplegar el servicio.


## Autor

- Pablo Jose Rivera
- Contacto: `<p.riverah@uniandes.edu.co>`