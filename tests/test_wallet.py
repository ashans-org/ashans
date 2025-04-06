
import pytest
from wallet.wallet import Wallet

def test_wallet_key_generation():
    wallet = Wallet()
    assert wallet.public_key is not None
    assert wallet.private_key is not None
