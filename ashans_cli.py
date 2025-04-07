import argparse
import time
import os
import base64
import hashlib
import pickle

from wallet.wallet import Wallet
from core.blockchain import Blockchain
from consensus.poa import ProofOfAuthority
from node.node import Node

wallet_instance = None
blockchain = None

WALLET_DIR = "wallet_data"
BLOCKCHAIN_FILE = "blockchain_data/chain.pkl"
PRIVATE_KEY_FILE = os.path.join(WALLET_DIR, "private.key")
PUBLIC_KEY_FILE = os.path.join(WALLET_DIR, "public.pem")

def save_wallet(wallet: Wallet):
    os.makedirs(WALLET_DIR, exist_ok=True)
    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(bytes(wallet.get_private_key()))
    with open(PUBLIC_KEY_FILE, "w") as f:
        f.write(wallet.get_public_key_pem())

def load_wallet() -> Wallet:
    if not os.path.exists(PRIVATE_KEY_FILE):
        return None
    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key_bytes = f.read()
    return Wallet.from_private_key(private_key_bytes)

def save_blockchain():
    os.makedirs("blockchain_data", exist_ok=True)
    with open(BLOCKCHAIN_FILE, "wb") as f:
        pickle.dump(blockchain, f)
    print("📝 Blockchain saved to disk.")

def load_blockchain(validators):
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return Blockchain(consensus=ProofOfAuthority(validators=validators))

def create_wallet():
    global wallet_instance
    wallet_instance = Wallet()
    save_wallet(wallet_instance)
    print("✅ Wallet created.")
    print("Public Key (PEM):")
    print(wallet_instance.get_public_key_pem())

def view_wallet():
    global wallet_instance
    wallet_instance = load_wallet()
    if not wallet_instance:
        print("❌ No wallet initialized.")
        return
    print("🔐 Wallet Info:")
    print("Address:", wallet_instance.get_address())
    print("Public Key (PEM):")
    print(wallet_instance.get_public_key_pem())

def simulate_floating_address():
    global wallet_instance
    wallet_instance = load_wallet()
    if not wallet_instance:
        print("❌ Wallet required. Use 'create-wallet' first.")
        return

    print("🔄 Simulating Floating Token Address every 10 seconds...")
    for _ in range(5):
        pub_key_pem = wallet_instance.get_public_key_pem()
        timestamp = str(int(time.time()))
        hashed = hashlib.sha256(pub_key_pem.encode() + timestamp.encode()).hexdigest()
        floating_address = base64.b64encode(hashed.encode()).decode()[:32]
        print(f"🧭 Floating Address: {floating_address}")
        time.sleep(10)

def viewBalance():
    global wallet_instance, blockchain
    wallet_instance = load_wallet()
    if not wallet_instance:
        print("❌ Wallet required. Use 'create-wallet' first.")
        return
    validators = [wallet_instance.get_public_key_pem()]
    blockchain = load_blockchain(validators)
    address = wallet_instance.get_address()
    balance = blockchain.get_balance(address)
    print(f"💰 Wallet Balance for {address}: {balance} coins")

def mineBlock():
    global wallet_instance, blockchain
    wallet_instance = load_wallet()
    if not wallet_instance:
        print("❌ Wallet required. Use 'create-wallet' first.")
        return

    validators = [wallet_instance.get_public_key_pem()]
    blockchain = load_blockchain(validators)

    # ✅ Ensure current wallet is added to validators if missing
    if wallet_instance.get_public_key_pem() not in blockchain.consensus.validators:
        blockchain.consensus.validators.append(wallet_instance.get_public_key_pem())

    node = Node(wallet=wallet_instance, blockchain=blockchain)

    transactions = [{"sender": "network", "recipient": wallet_instance.get_address(), "amount": 100}]
    block, proof = node.create_block(transactions)

    # ✅ Save only if block was actually added
    if block in blockchain.chain:
        save_blockchain()
        print("✅ Block mined and added to the blockchain.")
        print(block)
    else:
        print("❌ Block was not added. Check validator and consensus logic.")

def view_blockchain():
    global wallet_instance, blockchain
    wallet_instance = load_wallet()
    validators = [wallet_instance.get_public_key_pem()] if wallet_instance else []
    blockchain = load_blockchain(validators)

    print("📘 Blockchain State:")
    for block in blockchain.chain:
        print(block.__dict__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ashans CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("create-wallet", help="Generate a new wallet")
    subparsers.add_parser("view-wallet", help="View current wallet info")
    subparsers.add_parser("floating-token", help="Simulate floating token address")
    subparsers.add_parser("view-chain", help="View blockchain state")
    subparsers.add_parser("mine-block", help="Mine Block")
    subparsers.add_parser("view-balance", help="View Balance of Wallet")

    args = parser.parse_args()

    if args.command == "create-wallet":
        create_wallet()
    elif args.command == "view-wallet":
        view_wallet()
    elif args.command == "floating-token":
        simulate_floating_address()
    elif args.command == "view-chain":
        view_blockchain()
    elif args.command == "mine-block":
        mineBlock()
    elif args.command == "view-balance":
        viewBalance()
    else:
        parser.print_help()
