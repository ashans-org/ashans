from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

class ProofOfAuthority:
    def __init__(self, validators=None):
        self.validators = validators or []

    def sign(self, message, wallet):
        return wallet.sign(message)

    def get_proof(self, validator):
        # For PoA, the "proof" is just who signed the block (could also be a signature)
        return validator

    def validate_block(self, block):
        return block.validator in self.validators

    def verify_signature(self, message, signature, public_key_bytes):
        try:
            verify_key = VerifyKey(public_key_bytes)
            verify_key.verify(message, signature)
            return True
        except BadSignatureError:
            return False