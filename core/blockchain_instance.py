import os
import base64
import json
from nacl.secret import SecretBox
from nacl.utils import random as random_bytes
from wallet.wallet import Wallet
from core.blockchain import Blockchain
from consensus.poa import ProofOfAuthority

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WALLETS_DIR = os.path.join(BASE_DIR, "..", "wallets") 
VALIDATORS_JSON = "./validators.json"
DEFAULT_SECRET = base64.b64encode(b'supersecretkey!!1234567890123456')  # 32 bytes key

def load_validators(secret_key: bytes):
    validators = []
    validator_info = []
    os.makedirs(WALLETS_DIR, exist_ok=True)
    for filename in os.listdir(WALLETS_DIR):
        if filename.endswith(".wlt"):
            filepath = os.path.join(WALLETS_DIR, filename)
            try:
                wallet = Wallet.load_wallet_from_file(filepath, secret_key)
                validators.append(wallet)
                validator_info.append({
                    "address": wallet.get_address(),
                    "verify_key_b64": wallet.get_public_key_b64(),
                    "public_key_pem": wallet.get_public_key_pem()
                })
            except Exception as e:
                print(f"Failed to load validator from {filename}: {e}")

    # Save public validator info to a shared JSON file
    with open(VALIDATORS_JSON, 'w') as f:
        json.dump(validator_info, f, indent=2)

    return validators

# Load validators
validators = load_validators(base64.b64decode(DEFAULT_SECRET))

# Set up consensus
consensus = ProofOfAuthority(validators)

# Create Blockchain instance
blockchain_instance = Blockchain(consensus=consensus)

def store_to_blockchain(floating_address: str, encrypted_data: str):
    tx_id = blockchain_instance.add_transaction(
        sender="system",
        recipient=floating_address,
        amount=0,
        data=encrypted_data
    )
    blockchain_instance.mine()
    return tx_id

def get_data_from_blockchain(address: str):
    return blockchain_instance.get_data_by_address(address)
