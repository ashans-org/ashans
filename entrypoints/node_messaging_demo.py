import argparse
import time
from nacl.public import PrivateKey
from network.encryption import EncryptedChannel

def simulate_secure_communication():
    print("🔐 Initializing secure channels between Node A and Node B...")

    # Generate key pairs
    node_a_private = PrivateKey.generate()
    node_b_private = PrivateKey.generate()

    node_a_public = node_a_private.public_key
    node_b_public = node_b_private.public_key

    # Setup encrypted channels
    node_a_channel = EncryptedChannel(private_key=node_a_private, peer_public_key=node_b_public)
    node_b_channel = EncryptedChannel(private_key=node_b_private, peer_public_key=node_a_public)

    print("🔄 Secure channel established between nodes.")
    print("📡 Sending encrypted message from Node A to Node B...")

    message = "Hello from Node A!"
    encrypted = node_a_channel.encrypt(message.encode())
    time.sleep(1)  # Simulate network delay

    decrypted = node_b_channel.decrypt(encrypted).decode()
    print(f"✅ Node B received message: '{decrypted}'")

def main():
    parser = argparse.ArgumentParser(description="Ashans Node-to-Node Messaging Demo")
    parser.add_argument("--simulate", action="store_true", help="Run the secure communication simulation")
    args = parser.parse_args()

    if args.simulate:
        simulate_secure_communication()
    else:
        print("ℹ️ Use --simulate to run the secure communication demo.")

if __name__ == "__main__":
    main()