from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder

class EncryptionUtils:
    def __init__(self):
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key

    def encrypt(self, recipient_public_key: PublicKey, message: str) -> str:
        box = Box(self.private_key, recipient_public_key)
        encrypted = box.encrypt(message.encode(), encoder=Base64Encoder)
        return encrypted.decode()

    def decrypt(self, sender_public_key: PublicKey, encrypted_message: str) -> str:
        box = Box(self.private_key, sender_public_key)
        decrypted = box.decrypt(encrypted_message.encode(), encoder=Base64Encoder)
        return decrypted.decode()

    def get_public_key_bytes(self) -> bytes:
        return self.public_key.encode(encoder=Base64Encoder)

    @staticmethod
    def load_public_key(key_bytes: bytes) -> PublicKey:
        return PublicKey(key_bytes, encoder=Base64Encoder)
