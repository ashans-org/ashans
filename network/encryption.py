from nacl.public import PrivateKey, PublicKey, Box
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
class EncryptedChannel:
    def __init__(self, private_key=None, peer_public_key=None):
        self.private_key = private_key or PrivateKey.generate()
        self.public_key = self.private_key.public_key
        self.peer_public_key = peer_public_key
        self.box = Box(self.private_key, self.peer_public_key) if self.peer_public_key else None

    def set_key(self, peer_public_key):
        self.peer_public_key = peer_public_key
        self.box = Box(self.private_key, self.peer_public_key)

    def encrypt(self, message):
        if not self.box:
            raise ValueError("Encryption box not initialized. Call set_key() first.")
        return self.box.encrypt(message)

    def decrypt(self, encrypted_message):
        if not self.box:
            raise ValueError("Encryption box not initialized. Call set_key() first.")
        return self.box.decrypt(encrypted_message)