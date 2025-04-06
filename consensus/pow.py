import hashlib
import time

class ProofOfWork:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty  # Leading zeroes in the hash

    def mine(self, data):
        prefix = '0' * self.difficulty
        nonce = 0
        while True:
            guess = f"{data}{nonce}".encode()
            hash_result = hashlib.sha256(guess).hexdigest()
            if hash_result.startswith(prefix):
                return nonce, hash_result
            nonce += 1

    def validate(self, data, nonce):
        guess = f"{data}{nonce}".encode()
        hash_result = hashlib.sha256(guess).hexdigest()
        return hash_result.startswith('0' * self.difficulty)