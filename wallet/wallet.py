import os
import hashlib
from nacl.public import PrivateKey, PublicKey
from nacl.encoding import RawEncoder
from cryptography.hazmat.primitives import serialization

class Wallet:
    def __init__(self):
        self._private_key = PrivateKey.generate()
        self._public_key = self._private_key.public_key
        self.public_key_pem = self._serialize_public_key(self._public_key)

    def _serialize_public_key(self, public_key):
        return public_key.encode(encoder=RawEncoder).hex()

    def get_private_key(self):
        return self._private_key

    def get_public_key(self):
        return self._public_key

    def get_public_key_pem(self):
        return self.public_key_pem

    def get_address(self):
        return hashlib.sha256(self.public_key_pem.encode()).hexdigest()