import base64
import hashlib
import jwt
import time
from datetime import datetime, timedelta
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder
from .settings import SECRET_KEY, ALGORITHM

# Generate the signature for a given message using the wallet's signing key (NaCl)
def generate_signature(wallet, message):
    signing_key = wallet.get_signing_key()  # This returns the signing key
    print(f"Message being signed: {message}")
    signature = signing_key.sign(message.encode())  # Sign the message
    return signature.signature  # Return only the signature (64 bytes)

# Generate a JWT token based on wallet address (can include more claims as needed)
def generate_jwt_token(data, expires_delta: timedelta = timedelta(minutes=30)):
    if not isinstance(data, dict):
        raise ValueError("Expected data to be a dictionary")

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def generate_floating_address(public_key_pem: str, interval_seconds=30, offset=0) -> str:
    current_slot = int(time.time() // interval_seconds) + offset
    seed = f"{public_key_pem}|{current_slot}"
    hashed = hashlib.sha256(seed.encode()).digest()
    return base64.urlsafe_b64encode(hashed).decode()[:32]
