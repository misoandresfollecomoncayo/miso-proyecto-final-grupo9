from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_USER, DB_NAME, DB_PASSWORD, INSTANCE_CONNECTION_NAME, ENVIRONMENT, DB_HOST, DB_PORT
from .models import WebhookResponse, Test, Base
from google.cloud.sql.connector import Connector
import pg8000
from os import environ

if ENVIRONMENT == "dev":
    environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./apikey.json"
    db_url = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url)
else:
    connector = Connector()

    def getconn():
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )
        return conn

    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_pre_ping=True
    )

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def crear_registro_bd(webhook_response: WebhookResponse):
    session = Session()
    try:
        db_obj = Test(
            id_transaction=webhook_response.id_transaction,
            code=webhook_response.code,
            status=webhook_response.status,
            created_at=webhook_response.created_at
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
