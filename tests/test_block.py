
import pytest
from core.block import Block

def test_block_creation():
    block = Block(index=1, previous_hash='abc', transactions=[], timestamp=1234567890, nonce=0)
    assert block.index == 1
    assert block.previous_hash == 'abc'
