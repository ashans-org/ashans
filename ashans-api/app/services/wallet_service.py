import base64
import time
from nacl.signing import VerifyKey
from app.utils.jwt_utils import create_jwt_token
from fastapi import HTTPException

import hashlib
from nacl.public import PrivateKey
from nacl.hash import blake2b
from nacl.encoding import RawEncoder

class Wallet:
    def __init__(self, address):
        self.address = address

    def get_current_floating_keypair(self, interval_secs=30):
        return self._keypair_for_interval(int(time.time()) // interval_secs)

    def get_floating_keypair_offset(self, offset: int, interval_secs=30):
        current_interval = int(time.time()) // interval_secs + offset
        return self._keypair_for_interval(current_interval)

    def _keypair_for_interval(self, interval):
        seed = f"{self.address}-{interval}".encode()
        digest = blake2b(seed, encoder=RawEncoder)[:32]
        private_key = PrivateKey(digest)
        public_key = private_key.public_key
        floating_address = hashlib.sha3_256(public_key.encode() + str(interval).encode()).hexdigest()
        return floating_address, {
            "public_key": public_key,
            "private_key": private_key
        }

def get_wallet_from_user(user):
    return Wallet(user["address"])
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
