import argparse
import time
import os
import base64
import hashlib
import pickle
import json
import getpass

from wallet.wallet import Wallet
from core.blockchain import Blockchain
from consensus.poa import ProofOfAuthority
from node.node import Node
from network.messaging import EncryptedMessenger
from core.blockchain_instance import DEFAULT_SECRET, WALLETS_DIR
from utils.block_utils import sanitize_block
from utils.auth_utils import generate_signature, generate_jwt_token 

wallet_instance = None
blockchain = None
BLOCKCHAIN_FILE = "blockchain_data/chain.pkl"
VALIDATORS_JSON = "wallets/validators.json"


def save_validator_wallet(wallet: Wallet):
    os.makedirs(WALLETS_DIR, exist_ok=True)
    path = os.path.join(WALLETS_DIR, f"{wallet.address}.wlt")
    secret_key = base64.b64decode(DEFAULT_SECRET)
    wallet.save_wallet_to_file(path, secret_key)
    print(f"✅ Encrypted validator wallet saved to: {path}")


def create_wallet():
    global wallet_instance
    if wallet_instance is None:
        wallet_instance = Wallet()
        save_validator_wallet(wallet_instance)
        print("✅ Wallet created.")
        print("Address:", wallet_instance.get_address())
        print("Public Key (PEM):")
        print(wallet_instance.get_public_key_pem())


def list_wallets():
    if not os.path.exists(WALLETS_DIR):
        return []
    wallets = []
    for f in os.listdir(WALLETS_DIR):
        if f.endswith(".wlt"):
            wallets.append(f)
    return wallets


def select_and_unlock_wallet():
    global wallet_instance
    wallets = list_wallets()
    if not wallets:
        print("❌ No wallets found. Create one using 'create-wallet'.")
        return None

    print("👜 Available wallets:")
    for idx, wfile in enumerate(wallets):
        print(f"{idx + 1}: {wfile}")

    try:
        choice = int(input("Select wallet number: ")) - 1
        if choice < 0 or choice >= len(wallets):
            print("❌ Invalid selection.")
            return None
    except ValueError:
        print("❌ Invalid input.")
        return None

    password = getpass.getpass("🔐 Enter wallet password: ")
    path = os.path.join(WALLETS_DIR, wallets[choice])
    try:
        secret_key = base64.b64decode(DEFAULT_SECRET)
        wallet = Wallet.load_wallet_from_file(path, secret_key)
        wallet_instance = wallet
        print(f"🔓 Wallet loaded: {wallet.address}")
        return wallet
    except Exception as e:
        print(f"❌ Failed to load wallet: {str(e)}")
        return None


def load_blockchain(validators):
    global blockchain
    if blockchain is None:  # Only load if not already loaded
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, "rb") as f:
                blockchain = pickle.load(f)
        else:
            blockchain = Blockchain(consensus=ProofOfAuthority(validators=validators))
    return blockchain


def save_blockchain():
    os.makedirs("blockchain_data", exist_ok=True)
    with open(BLOCKCHAIN_FILE, "wb") as f:
        pickle.dump(blockchain, f)
    print("📝 Blockchain saved to disk.")


def view_wallet():
    global wallet_instance
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    if wallet_instance:
        print("🔐 Wallet Info:")
        print("Address:", wallet_instance.get_address())
        print("Public Key (PEM):")
        print(wallet_instance.get_public_key_pem())
    else:
        print("❌ No wallet loaded.")


def simulate_floating_address():
    global wallet_instance
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    if wallet_instance:
        print("🔄 Simulating Floating Token Address every 10 seconds...")
        for _ in range(5):
            pub_key_pem = wallet_instance.get_public_key_pem()
            timestamp = str(int(time.time()))
            hashed = hashlib.sha256(pub_key_pem.encode() + timestamp.encode()).hexdigest()
            floating_address = base64.b64encode(hashed.encode()).decode()[:32]
            print(f"🧭 Floating Address: {floating_address}")
            time.sleep(10)
    else:
        print("❌ No wallet loaded.")


def viewBalance():
    global wallet_instance, blockchain
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    if wallet_instance:
        validators = [wallet_instance.get_public_key_pem()]
        blockchain = load_blockchain(validators)
        address = wallet_instance.get_address()
        balance = blockchain.get_balance(address)
        print(f"💰 Wallet Balance for {address}: {balance} coins")
    else:
        print("❌ No wallet loaded.")


def mineBlock():
    global wallet_instance, blockchain
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    if wallet_instance:
        validators = [wallet_instance.get_public_key_pem()]
        blockchain = load_blockchain(validators)

        if wallet_instance.get_public_key_pem() not in blockchain.consensus.validators:
            blockchain.consensus.validators.append(wallet_instance.get_public_key_pem())

        node = Node(wallet=wallet_instance, blockchain=blockchain)

        transactions = [{"sender": "network", "recipient": wallet_instance.get_address(), "amount": 100}]
        block, proof = node.create_block(transactions)

        if block in blockchain.chain:
            save_blockchain()
            print("✅ Block mined and added to the blockchain.")
            print(json.dumps(sanitize_block(block), indent=2))
        else:
            print("❌ Block was not added. Check validator and consensus logic.")
    else:
        print("❌ No wallet loaded.")


def view_blockchain():
    global wallet_instance, blockchain
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    validators = [wallet_instance.get_public_key_pem()] if wallet_instance else []
    blockchain = load_blockchain(validators)

    print("📘 Blockchain State:")
    for block in blockchain.chain:
        print(json.dumps(sanitize_block(block), indent=2))


def init_node():
    global wallet_instance
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    if wallet_instance:
        messenger = EncryptedMessenger(wallet_instance)
        print("✅ Node initialized for messaging.")
    else:
        print("❌ No wallet loaded.")


def send_message():
    global wallet_instance
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    if wallet_instance:
        recipient_pub_key = input("🔑 Enter recipient public key PEM: ")
        message = input("✉️  Enter your message: ")

        messenger = EncryptedMessenger(wallet_instance)
        encrypted_message = messenger.encrypt_message(recipient_pub_key, message)

        print("🔒 Encrypted Message:", encrypted_message)
    else:
        print("❌ No wallet loaded.")


def receive_message():
    global wallet_instance
    if wallet_instance is None:
        wallet_instance = select_and_unlock_wallet()
    if wallet_instance:
        encrypted_input = input("📩 Paste received encrypted message: ")
        messenger = EncryptedMessenger(wallet_instance)
        decrypted = messenger.decrypt_message(encrypted_input)

        print("📬 Decrypted message:", decrypted)
    else:
        print("❌ No wallet loaded.")


def generate_login_payload(wallet: Wallet, message: str = "login to wallet"):
    # Generate the login payload with the message and signature
    public_key_pem = wallet.get_public_key_pem()
    signature = generate_signature(wallet, message)  # Assume this function is implemented
    signature_b64 = base64.b64encode(signature).decode() 
    login_payload = {
        "address": wallet.get_address(),
        "public_key": public_key_pem,
        "message": message,
        "signature": signature_b64
    }
    return login_payload


def serialize_wallet_response(response):
    # Ensure the response is serializable
    if isinstance(response, dict):
        # If it's a dictionary, recursively handle each value
        return {key: serialize_wallet_response(value) for key, value in response.items()}
    
    elif isinstance(response, bytes):
        # If the object is bytes, convert it to base64
        return base64.b64encode(response).decode()
    
    # Add more cases as needed for other custom objects
    return response  # Return if it's already a serializable type (e.g., string, int)


def create_wallet_json():
    global wallet_instance
    if wallet_instance is None:
        # Create a new wallet instance
        wallet_instance = Wallet()

        # Save the wallet to a file with encryption
        save_validator_wallet(wallet_instance)

    wallet_address = wallet_instance.get_address()
    wallet_public_key = wallet_instance.get_public_key_pem()

    login_payload = generate_login_payload(wallet_instance)

    # Generate JWT token for authentication
    token = generate_jwt_token({"address": wallet_address})  # Assume you have this function implemented

    # Format the JSON response similar to the REST API
    response = {
        "address": wallet_address,
        "public_key": wallet_public_key,
        "login_payload": login_payload,
        "token": token
    }
    serializable_response = serialize_wallet_response(response)
    # Print the JSON response
    print(json.dumps(serializable_response, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ashans CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("create-wallet", help="Generate a new wallet")
    subparsers.add_parser("view-wallet", help="View wallet details")
    subparsers.add_parser("mine-block", help="Mine a block")
    subparsers.add_parser("simulate-floating-address", help="Simulate floating token address")
    subparsers.add_parser("view-balance", help="View wallet balance")
    subparsers.add_parser("view-blockchain", help="View the current blockchain")
    subparsers.add_parser("init-node", help="Initialize a node for messaging")
    subparsers.add_parser("send-message", help="Send an encrypted message")
    subparsers.add_parser("receive-message", help="Receive and decrypt a message")
    subparsers.add_parser("create-wallet-json", help="Create wallet and return JSON login response")

    args = parser.parse_args()

    if args.command == "create-wallet":
        create_wallet()
    elif args.command == "view-wallet":
        view_wallet()
    elif args.command == "mine-block":
        mineBlock()
    elif args.command == "simulate-floating-address":
        simulate_floating_address()
    elif args.command == "view-balance":
        viewBalance()
    elif args.command == "view-blockchain":
        view_blockchain()
    elif args.command == "init-node":
        init_node()
    elif args.command == "send-message":
        send_message()
    elif args.command == "receive-message":
        receive_message()
    elif args.command == "create-wallet-json":
        create_wallet_json()

