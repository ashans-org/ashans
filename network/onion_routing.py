
import random
from network.secure_communication import NodeCommunicator
import os

class OnionNode:
    def __init__(self, node_id, shared_key):
        self.node_id = node_id
        self.communicator = NodeCommunicator(shared_key)

    def wrap_message(self, message, path_nodes):
        # Wraps the message in multiple encryption layers for onion routing
        payload = message
        for node in reversed(path_nodes):
            payload = node.communicator.encrypt_message(payload)
        return payload

    def unwrap_message(self, wrapped_msg):
        return self.communicator.decrypt_message(wrapped_msg)

# Simulated Onion Routing Network
if __name__ == "__main__":
    # Shared secret key (in real cases this would be key-exchanged securely)
    shared_key = os.urandom(32)

    # Simulate 3 relay nodes
    nodes = [OnionNode(f"relay_{i}", shared_key) for i in range(3)]

    # Sender wraps message with all node layers
    sender = OnionNode("sender", shared_key)
    original_msg = "Final secure message to target node"
    onion_encrypted = sender.wrap_message(original_msg, nodes)

    print("Onion Encrypted Message:", onion_encrypted)

    # Each node peels off one layer
    for i, node in enumerate(nodes):
        onion_encrypted = node.unwrap_message(onion_encrypted)
        print(f"Node {node.node_id} peeled one layer.")

    print("Final Decrypted Message:", onion_encrypted)
