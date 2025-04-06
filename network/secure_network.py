from nacl.public import PrivateKey, PublicKey, Box, SealedBox
import base64
class EncryptedChannel:
    def __init__(self, private_key=None, peer_public_key=None):
        self.private_key = private_key or PrivateKey.generate()
        self.public_key = self.private_key.public_key
        self.peer_public_key = peer_public_key
        self.box = Box(self.private_key, self.peer_public_key) if self.peer_public_key else None

    def set_key(self, peer_public_key):
        self.peer_public_key = peer_public_key
        self.box = Box(self.private_key, self.peer_public_key)

    def encrypt(self, message: bytes) -> bytes:
        if not self.box:
            raise ValueError("Encryption box not initialized for encryption. Call set_key() first.")
        return self.box.encrypt(message)

    def decrypt(self, encrypted_message: bytes) -> bytes:
        if self.box:
            return self.box.decrypt(encrypted_message)
        else:
            # Fallback for onion layer or messages without known peer key
            sealed_box = SealedBox(self.private_key)
            return sealed_box.decrypt(encrypted_message)

class OnionPacket:
    def __init__(self, payload: bytes, path: list[str]):
        self.payload = payload
        self.path = path  # list of public keys (base64-encoded)

    def wrap_layers(self) -> bytes:
        data = self.payload
        for pubkey_b64 in reversed(self.path):
            pubkey = PublicKey(base64.b64decode(pubkey_b64))
            sealed_box = SealedBox(pubkey)
            data = sealed_box.encrypt(data)
        return data

    @staticmethod
    def unwrap_layer(encrypted_data: bytes, private_key: PrivateKey) -> bytes:
        sealed_box = SealedBox(private_key)
        return sealed_box.decrypt(encrypted_data)