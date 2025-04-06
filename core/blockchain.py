class EncryptedBlock:
    def __init__(self, previous_hash, data, nonce):
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce

class MessageBlockchain:
    def __init__(self):
        self.chain = []
