from fastapi import APIRouter, Depends
from app.services.auth import get_current_user

router = APIRouter(prefix="/mine", tags=["mining"])

@router.post("/block")
def mine_block(user=Depends(get_current_user)):
    return {"status": "block mined", "user": user}