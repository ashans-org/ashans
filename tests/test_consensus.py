
import pytest
from consensus.pow import ProofOfWork

def test_proof_of_work_difficulty():
    pow = ProofOfWork(difficulty=3)
    nonce, hash_result = pow.mine("some test data")
    assert hash_result.startswith('0' * 3)
