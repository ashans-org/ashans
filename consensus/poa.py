
import hashlib
import hmac
import time
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AuthorityNode:
    def __init__(self, node_id, secret_key):
        self.node_id = node_id
        self.secret_key = secret_key
        self.ec_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
        self.public_key = self.ec_key.public_key()

    def sign_block(self, block_data):
        block_hash = hashlib.sha256(block_data.encode()).digest()
        signature = self.ec_key.sign(block_hash, ec.ECDSA(hashes.SHA256()))
        return signature

    def verify_signature(self, block_data, signature, public_key):
        try:
            public_key.verify(signature, hashlib.sha256(block_data.encode()).digest(), ec.ECDSA(hashes.SHA256()))
            return True
        except Exception:
            return False

    def encrypt_with_hmac(self, data):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = kdf.derive(self.secret_key.encode())
        return hmac.new(key, data.encode(), hashlib.sha256).hexdigest(), salt.hex()

class PoAValidator:
    def __init__(self):
        self.authority_nodes = {}

    def register_node(self, node_id, secret_key):
        node = AuthorityNode(node_id, secret_key)
        self.authority_nodes[node_id] = node
        return node

    def validate_block(self, node_id, block_data, signature):
        node = self.authority_nodes.get(node_id)
        if not node:
            return False
        return node.verify_signature(block_data, signature, node.public_key)
