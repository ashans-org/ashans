from core.node import Node
from core.blockchain import Blockchain
from consensus.poa import ProofOfAuthority
from network.encryption import EncryptedChannel
from wallet.wallet import Wallet
import time

def main():
    print("🔗 Welcome to the Ashans Blockchain Node")
    
    # Step 1: Initialize Wallet
    wallet = Wallet()
    print("🪪 Wallet initialized with public key:")
    print(wallet.get_public_key_pem().decode())

    # Step 2: Setup Blockchain and PoA
    poa = ProofOfAuthority(validators=[wallet.get_public_key_pem()])
    blockchain = Blockchain(consensus=poa)
    print("🚀 Blockchain and Proof of Authority consensus initialized.")

    # Step 3: Initialize Secure Channel (Simulated)
    secure_channel = EncryptedChannel()
    secure_channel.set_key(wallet.public_key)
    print("🔐 Encrypted channel initialized.")

    # Step 4: Initialize Network Node
    node = Node(wallet=wallet, blockchain=blockchain, channel=secure_channel)
    print("🌐 Node is up and running.")

    # Step 5: Simulate floating address logic
    while True:
        node.update_floating_address()
        print(f"🔄 New floating address: {node.floating_address}")
        time.sleep(10)

if __name__ == "__main__":
    main()