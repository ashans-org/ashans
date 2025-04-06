
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

class NodeCommunicator:
    def __init__(self, shared_key: bytes):
        self.shared_key = shared_key[:32]  # Ensure 256-bit key

    def encrypt_message(self, plaintext: str) -> str:
        iv = os.urandom(16)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.shared_key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(iv + encrypted).decode()

    def decrypt_message(self, encrypted_message: str) -> str:
        raw = base64.b64decode(encrypted_message)
        iv = raw[:16]
        ciphertext = raw[16:]

        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.shared_key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode()

# Example usage (simulation of secure node-to-node messaging)
if __name__ == "__main__":
    key = os.urandom(32)
    node1 = NodeCommunicator(key)
    node2 = NodeCommunicator(key)

    original_msg = "This is a secure message between nodes."
    encrypted = node1.encrypt_message(original_msg)
    decrypted = node2.decrypt_message(encrypted)

    print("Encrypted Message:", encrypted)
    print("Decrypted Message:", decrypted)
