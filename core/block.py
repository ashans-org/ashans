import time
import hashlib
import json

class Block:
    def __init__(self, index, previous_hash, timestamp=None, transactions=None, nonce=0,validator = None,consensus=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions or []
        self.nonce = nonce
        self.hash = self.compute_hash()
        self.validator = validator
        self.consensus=consensus

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
