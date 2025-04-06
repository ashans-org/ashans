from nacl.public import PrivateKey, PublicKey, Box, SealedBox
import base64
class EncryptedChannel:
    def __init__(self, private_key=None):
        self.private_key = private_key or PrivateKey.generate()
        self.public_key = self.private_key.public_key

    def create_box(self, peer_public_key):
        return Box(self.private_key, peer_public_key)

    def set_key(self, peer_public_key):
        self.peer_public_key = peer_public_key
        self.box = Box(self.private_key, self.peer_public_key)

    def encrypt(self, peer_public_key, message: bytes) -> bytes:
        box = Box(self.private_key, peer_public_key)
        return box.encrypt(message)

    def decrypt(self, sender_public_key, encrypted_message: bytes) -> bytes:
        box = Box(self.private_key, sender_public_key)
        return box.decrypt(encrypted_message)


class OnionPacket:
    def __init__(self, payload: bytes, path: list):
        self.payload = payload
        self.path = path

    def encrypt_layer(self, recipient_pubkey: PublicKey, sender_privkey: PrivateKey) -> bytes:
        box = Box(sender_privkey, recipient_pubkey)
        encrypted = box.encrypt(self.payload)
        return sender_privkey.public_key.encode() + encrypted  # prepend sender pubkey
    
    @staticmethod
    def unwrap_layer(private_key: PrivateKey, encrypted_layer: bytes) -> bytes:
        sender_pubkey = PublicKey(encrypted_layer[:32])
        encrypted_message = encrypted_layer[32:]
        box = Box(private_key, sender_pubkey)
        return box.decrypt(encrypted_message)