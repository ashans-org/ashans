import os
import json
import base64
import hashlib
from nacl.public import PrivateKey, PublicKey
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import Base64Encoder
from nacl.secret import SecretBox
from nacl.hash import blake2b


class Wallet:
    def __init__(self, private_key=None, signing_key=None):
        # For encryption: NaCl's PrivateKey (used for encryption/decryption)
        self.private_key = PrivateKey.generate() if private_key is None else PrivateKey(private_key)
        self.public_key = self.private_key.public_key

        # For signing: NaCl's SigningKey (used for signing messages)
        self.signing_key = SigningKey.generate() if signing_key is None else SigningKey(signing_key)
        self.verify_key = self.signing_key.verify_key

        # Public key PEM and address
        self.public_key_pem = base64.b64encode(bytes(self.public_key)).decode()
        self.address = hashlib.sha256(self.verify_key.encode()).hexdigest()

    def get_private_key(self):
        # Return the raw private key bytes
        return bytes(self.private_key)

    def get_signing_key(self):
        return self.signing_key

    def get_verify_key(self):
        return self.verify_key

    def get_public_key(self):
        return self.public_key

    def get_public_key_pem(self):
        return self.public_key_pem

    def get_address(self):
        return hashlib.sha256(self.get_public_key_pem().encode()).hexdigest()

    def sign(self, message: str) -> bytes:
        """
        Sign a message using the signing key and return the signature.
        """
        signed = self.signing_key.sign(message.encode())
        return signed.signature  # Only return the 64-byte signature

    def verify(self, message: str, signature: bytes) -> bool:
        """
        Verify a message's signature using the verify key.
        """
        try:
            self.verify_key.verify(message.encode(), signature)
            return True
        except Exception:
            return False

    def get_public_key_b64(self):
        """
        Return the base64-encoded public key for the wallet's signing key.
        """
        return base64.b64encode(self.verify_key.encode()).decode()

    def _generate_address(self):
        return hashlib.sha256(self.verify_key.encode()).hexdigest()

    @staticmethod
    def load_wallet_from_file(filepath: str, secret_key: bytes):
        """
        Load an encrypted wallet file using SecretBox and return a Wallet instance.
        """
        box = SecretBox(secret_key)

        with open(filepath, 'rb') as f:
            encrypted_data = f.read()

        decrypted = box.decrypt(encrypted_data)
        wallet_data = json.loads(decrypted.decode())

        private_key = base64.b64decode(wallet_data['private_key'])
        signing_key = base64.b64decode(wallet_data['signing_key'])

        return Wallet(private_key=private_key, signing_key=signing_key)

    def save_wallet_to_file(self, filepath: str, secret_key: bytes):
        """
        Save wallet keys to an encrypted file using SecretBox.
        """
        box = SecretBox(secret_key)

        wallet_data = {
            'private_key': base64.b64encode(bytes(self.private_key)).decode(),
            'signing_key': base64.b64encode(self.signing_key.encode()).decode()
        }

        json_data = json.dumps(wallet_data).encode()
        encrypted = box.encrypt(json_data)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(encrypted)
