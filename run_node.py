from network.node import Node
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()  # Load from .env

    port = os.getenv("NODE_PORT", "5000")
    difficulty = os.getenv("DIFFICULTY", "5")
    floating_interval = os.getenv("FLOATING_ADDRESS_INTERVAL", "10")
    rotation_interval = os.getenv("ADDRESS_ROTATION_INTERVAL", "30")

    print(f"Starting node on port {port} with difficulty {difficulty}")
    print(f"Floating token interval: {floating_interval}s, Address rotation interval: {rotation_interval}s")

    node = Node()
    node.start()
