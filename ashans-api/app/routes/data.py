from fastapi import APIRouter, Depends
from app.services.auth import get_current_user

router = APIRouter(prefix="/data", tags=["data"])

database = {}

@router.post("/store")
def store_data(payload: dict, user=Depends(get_current_user)):
    database[user] = payload
    return {"status": "data stored"}

@router.get("/retrieve")
def retrieve_data(user=Depends(get_current_user)):
    return database.get(user, {})