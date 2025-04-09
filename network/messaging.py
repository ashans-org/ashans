import base64
from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.encoding import Base64Encoder
from nacl.exceptions import CryptoError, ValueError as NaClValueError, TypeError as NaClTypeError
import binascii

class EncryptedMessenger:
    def __init__(self, wallet):
        self.wallet = wallet
        self.private_key = wallet.get_private_key()
        self.public_key = wallet.get_public_key()

    def encrypt_message(self, recipient_pub_key_pem, message: str) -> str:
        try:
            b64_data = recipient_pub_key_pem.strip().encode()
            recipient_pub_key_bytes = base64.b64decode(b64_data)
            recipient_pub_key = PublicKey(recipient_pub_key_bytes)
            sealed_box = SealedBox(recipient_pub_key)
            encrypted = sealed_box.encrypt(message.encode(), encoder=Base64Encoder)
            return encrypted.decode()
        except binascii.Error:
            return "❌ Invalid Base64 encoding in recipient public key."
        except NaClValueError as e:
            return f"❌ Public key error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected encryption error: {str(e)}"

    def decrypt_message(self, encrypted_message_b64: str) -> str:
        try:
            sealed_box = SealedBox(self.private_key)
            decrypted = sealed_box.decrypt(encrypted_message_b64.encode(), encoder=Base64Encoder)
            return decrypted.decode()
        except NaClTypeError:
            return "❌ Encrypted message too short or corrupted."
        except CryptoError:
            return "❌ Unable to decrypt message. Possibly wrong recipient or malformed ciphertext."
        except Exception as e:
            return f"❌ Unexpected decryption error: {str(e)}"
