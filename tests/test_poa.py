from nacl.signing import SigningKey
from consensus.poa import ProofOfAuthority

def test_validator_signature_and_verification():
    sk = SigningKey.generate()
    vk = sk.verify_key
    message = b"hello world"
    signature = sk.sign(message).signature

    poa = ProofOfAuthority()
    assert poa.verify_signature(message, signature, vk.encode()) is True