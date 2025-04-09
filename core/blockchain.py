# Updated core/blockchain.py
import time
import hashlib
import json
import os
from nacl.public import SealedBox
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey
from nacl.secret import SecretBox
from nacl.utils import random as nacl_random
from utils.block_utils import sanitize_block

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0, validator=None):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.validator = self._serialize_validator(validator)
        self.hash = self.compute_hash()

    def _serialize_validator(self, validator):
        try:
            return validator.address if hasattr(validator, 'address') else str(validator)
        except Exception:
            return str(validator)

    def compute_hash(self):
        block_data = sanitize_block(self)
        # Remove the hash field before hashing (if exists)
        if "hash" in block_data:
            del block_data["hash"]
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()

    def __str__(self):
        return json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "validator": self.validator,
            "hash": self.hash
        }, indent=2)

    def __repr__(self):
        return self.__str__()


class Blockchain:
    difficulty = 3

    def __init__(self, consensus=None):
        self.consensus = consensus
        self.chain = []
        self.unconfirmed_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        validator = self.consensus.validators[0] if self.consensus and self.consensus.validators else "genesis"
        genesis_block = Block(
            index=0,
            transactions=[],
            timestamp=time.time(),
            previous_hash="0",
            validator=validator
        )
        genesis_block.hash = self.proof_of_work(genesis_block)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.get_last_block().hash

        if self.consensus and not self.consensus.validate_block(block):
            raise Exception("Block rejected: invalid validator")

        if previous_hash != block.previous_hash:
            return False

        if hasattr(self.consensus, "is_valid_proof"):
            if not self.consensus.is_valid_proof(block, proof):
                return False
        else:
            if not self.is_valid_proof(block, proof):
                return False

        block.hash = block.compute_hash()
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return block_hash.startswith("0" * Blockchain.difficulty) and block_hash == block.compute_hash()

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            timestamp=time.time(),
            previous_hash=last_block.hash,
            validator=self.consensus.validators[0] if self.consensus and self.consensus.validators else "auto"
        )
        proof = self.proof_of_work(new_block)
        added = self.add_block(new_block, proof)
        if added:
            self.unconfirmed_transactions = []
            print(f"Block #{new_block.index} mined with hash: {new_block.hash}")
            return new_block.index
        return False

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                sender = tx.get("from") or tx.get("sender")
                recipient = tx.get("to") or tx.get("recipient")
                amount = tx.get("amount", 0)
                if recipient == address:
                    balance += amount
                if sender == address:
                    balance -= amount
        return balance

    def get_data_by_address(self, address, limit=3):
        results = []
        for block in reversed(self.chain):
            for tx in block.transactions:
                if tx.get("type") == "data" and tx.get("from") == address:
                    results.append({
                        "block": block.index,
                        "payload": tx["payload"],
                        "timestamp": block.timestamp
                    })
                    if len(results) >= limit:
                        return results
        return results

# External shared interface

def store_to_blockchain(address, encrypted_b64):
    from core.blockchain_instance import blockchain_instance
    transaction = {
        "type": "data",
        "from": address,
        "to": "data_store",
        "payload": encrypted_b64
    }
    blockchain_instance.add_transaction(transaction)
    blockchain_instance.mine()
