# ashans-api/app/routes/wallet.py

from fastapi import APIRouter, Request, HTTPException
from app.utils.jwt_utils import create_jwt_token
from wallet.wallet import Wallet
from core.blockchain_instance import DEFAULT_SECRET, WALLETS_DIR
import base64
import os

router = APIRouter()

@router.post("/create-wallet")
async def create_wallet():
    try:
        wallet = Wallet()
        message = "login to wallet"
        signature = wallet.sign(message)  # returns bytes
        signature_b64 = base64.b64encode(signature).decode()

        # 🔐 Save encrypted validator wallet
        os.makedirs(WALLETS_DIR, exist_ok=True)
        filepath = os.path.join(WALLETS_DIR, f"{wallet.address}.wlt")
        wallet.save_wallet_to_file(filepath, base64.b64decode(DEFAULT_SECRET))

        login_payload = {
            "address": wallet.address,
            "public_key": wallet.get_public_key_b64(),
            "message": message,
            "signature": signature_b64
        }

        token = create_jwt_token({"address": wallet.address})

        return {
            "address": wallet.address,
            "public_key": wallet.get_public_key_b64(),
            "login_payload": login_payload,
            "token": token
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login_with_signature(request: Request):
    data = await request.json()
    login_payload = data.get("login_payload")

    if not login_payload:
        raise HTTPException(status_code=400, detail="Missing fields in login payload.")

    try:
        from app.services.wallet_service import verify_signature_and_issue_token
        return verify_signature_and_issue_token(login_payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
