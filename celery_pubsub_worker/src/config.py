import os

PROJECT_ID = os.getenv("PROJECT_ID", "testproyectointegrador-488523")
TOPIC_ID = os.getenv("TOPIC_ID", "payments-service-queue")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID", "payments-service-queue-sub")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "payment_service_db_test")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "testproyectointegrador-488523:us-central1:mi-postgres-instance")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

