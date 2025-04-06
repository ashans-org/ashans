from nacl.public import PrivateKey, PublicKey, Box
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
            raise ValueError("Encryption box not initialized.")
        return self.box.encrypt(message)

    def decrypt(self, encrypted_message: bytes) -> bytes:
        if not self.box:
            raise ValueError("Encryption box not initialized.")
        return self.box.decrypt(encrypted_message)

class OnionPacket:
    def __init__(self, payload: bytes, path: list[str]):
        self.payload = payload
        self.path = path  # List of public keys as base64 strings

    def wrap_layers(self):
        data = self.payload
        for pubkey_b64 in reversed(self.path):
            pubkey = PublicKey(base64.b64decode(pubkey_b64))
            channel = EncryptedChannel(peer_public_key=pubkey)
            data = channel.encrypt(data)
        return data

    @staticmethod
    def unwrap_layer(encrypted_data: bytes, private_key: PrivateKey) -> bytes:
        channel = EncryptedChannel(private_key)
        return channel.decrypt(encrypted_data)
