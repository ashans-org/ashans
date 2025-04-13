# models/schemas.py
from pydantic import BaseModel
from typing import Any, Dict

class StoreDataRequest(BaseModel):
    data: str

class StoreDataResponse(BaseModel):
    message: str
    block: Dict[str, Any]

class RetrieveDataResponse(BaseModel):
    data: Dict[str, Any]
