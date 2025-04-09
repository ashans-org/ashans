import base64
from nacl.signing import VerifyKey
from app.utils.jwt_utils import create_jwt_token
from fastapi import HTTPException

def verify_signature_and_issue_token(data: dict):
    try:
        address = data["address"]
        signature_b64 = data["signature"]
        message = data["message"]
        public_key_b64 = data["public_key"]

        public_key_bytes = base64.b64decode(public_key_b64)
        signature_bytes = base64.b64decode(signature_b64)

        if len(signature_bytes) != 64:
            raise HTTPException(status_code=400, detail="The signature must be exactly 64 bytes long")

        verify_key = VerifyKey(public_key_bytes)
        verify_key.verify(message.encode(), signature_bytes)
        address_dict = {"address": address}
        token = create_jwt_token(address_dict)
        return {"token": token}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verifying signature: {str(e)}")
