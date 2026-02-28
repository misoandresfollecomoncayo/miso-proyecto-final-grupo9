from pydantic import BaseModel
from datetime import datetime

class WebhookResponse(BaseModel):
    id_transaction : str
    code : int
    status : str
    created_at : datetime | None = None