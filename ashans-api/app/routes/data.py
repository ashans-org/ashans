from fastapi import APIRouter, Depends, HTTPException
from app.services.auth import get_current_user
from app.services.wallet_service import get_wallet_from_user
from core.blockchain_instance import store_to_blockchain
from nacl.public import SealedBox
import base64
import json

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/store")
def store_encrypted_data(payload: dict, user=Depends(get_current_user)):
    wallet = get_wallet_from_user(user)
    floating_address, keys = wallet.get_current_floating_keypair()
    public_key = keys["public_key"]

    tx_id = store_to_blockchain(
        data=payload,
        from_address=floating_address,
        public_key=public_key,
        format="json"
    )
    return {"status": "stored", "tx_id": tx_id, "address": floating_address}


@router.get("/retrieve")
def retrieve_data(user=Depends(get_current_user)):
    from core.blockchain_instance import blockchain_instance

    wallet = get_wallet_from_user(user)
    data_found = []

    for offset in range(0, 3):  # Current and last 2 address intervals
        floating_address, keys = wallet.get_floating_keypair_offset(-offset)
        private_key = keys["private_key"]

        # 🔍 Search blockchain for matching transaction(s)
        for block in blockchain_instance.chain:
            for tx in block.transactions:
                if tx.get("type") == "data" and tx.get("from") == floating_address:
                    try:
                        encrypted_b64 = tx["payload"]
                        encrypted = base64.b64decode(encrypted_b64)
                        box = SealedBox(private_key)
                        decrypted = box.decrypt(encrypted)
                        payload = json.loads(decrypted.decode())

                        data_found.append({
                            "block": block.index,
                            "address": floating_address,
                            "data": payload
                        })
                    except Exception:
                        continue

    if not data_found:
        raise HTTPException(status_code=404, detail="No data found in last 3 intervals")

    return data_found
