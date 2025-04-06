from nacl.public import PrivateKey, PublicKey, Box, SealedBox
import base64
class EncryptedChannel:
    def __init__(self, private_key=None):
        self.private_key = private_key or PrivateKey.generate()
        self.public_key = self.private_key.public_key

    def encrypt(self, peer_public_key, message):
        print(f"[Debug] Encrypting with key: {self.private_key.encode().hex()}")
        box = Box(self.private_key, peer_public_key)
        return self.public_key.encode() + box.encrypt(message)

    def decrypt(self, encrypted_message):
        sender_public_key = PublicKey(encrypted_message[:32])
        print(f"[Debug] Decrypting with key: {self.private_key.encode().hex()}")
        ciphertext = encrypted_message[32:]
        box = Box(self.private_key, sender_public_key)
        return box.decrypt(ciphertext)

class OnionPacket:
    def __init__(self, data: bytes):
        self.data = data

    def encrypt_layer(self, public_key):
        ephemeral_private_key = PrivateKey.generate()
        box = Box(ephemeral_private_key, public_key)
        return ephemeral_private_key.public_key.encode() + box.encrypt(self.data)

    @staticmethod
    def unwrap_layer(encrypted_payload: bytes, private_key):
        sender_pub_key = PublicKey(encrypted_payload[:32])
        message = encrypted_payload[32:]
        box = Box(private_key, sender_pub_key)
        return box.decrypt(message)