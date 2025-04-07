import os
import base64
import hashlib
from nacl.public import PrivateKey, PublicKey
from nacl.encoding import RawEncoder
from cryptography.hazmat.primitives import serialization

class Wallet:
    def __init__(self, private_key=None):
        if private_key is None:
            self.private_key = PrivateKey.generate()
        elif isinstance(private_key, bytes):
            self.private_key = PrivateKey(private_key)
        else:
            self.private_key = private_key  # Already a PrivateKey instance
        self.public_key = self.private_key.public_key
        self.public_key_pem = base64.b64encode(bytes(self.public_key)).decode()

    def _serialize_public_key(self, public_key):
        return public_key.encode(encoder=RawEncoder).hex()

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self._public_key

    def get_public_key_pem(self):
        return self.public_key_pem

    def get_address(self):
        return hashlib.sha256(self.get_public_key_pem().encode()).hexdigest()

    @classmethod
    def from_private_key(cls, private_key_bytes):
        private_key = PrivateKey(private_key_bytes)
        return cls(private_key)