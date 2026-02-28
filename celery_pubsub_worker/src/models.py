from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime, timezone
from pydantic import BaseModel
from datetime import datetime

class WebhookResponse(BaseModel):
    id_transaction : str
    code : int
    status : str
    created_at : datetime

Base = declarative_base()

class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key = True)
    id_transaction = Column(String(80), nullable=False)
    code = Column(Integer, nullable=False)
    status = Column(String(80), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    finished_at = Column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc).isoformat(), nullable=False)