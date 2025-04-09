import base64
import hashlib
import jwt
from datetime import datetime, timedelta
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder
from .settings import SECRET_KEY, ALGORITHM

# Generate the signature for a given message using the wallet's signing key (NaCl)
def generate_signature(wallet, message):
    signing_key = wallet.get_signing_key()  # This returns the signing key
    signature = signing_key.sign(message.encode())  # Sign the message
    return signature.signature  # Return only the signature (64 bytes)

# Generate a JWT token based on wallet address (can include more claims as needed)
def generate_jwt_token(payload):
    secret_key = SECRET_KEY  # Should be kept secure and not hardcoded
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {**payload, "exp": expiration}, 
        secret_key, 
        algorithm=ALGORITHM
    )
    return token
