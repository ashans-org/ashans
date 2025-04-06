import base64
from network.secure_network import EncryptedChannel, OnionPacket
from nacl.public import PublicKey
from nacl.exceptions import CryptoError


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.channel = EncryptedChannel()
        self.network = {}

    def receive(self, encrypted_payload):
        try:
            decrypted = OnionPacket.unwrap_layer(encrypted_payload, self.channel.private_key)
            print(f"[{self.node_id}] ✅ Decrypted a layer.")
            header, _, payload = decrypted.partition(b"\n")
            if header.startswith(b"HOP:"):
                next_node_id = header[4:].decode()
                if next_node_id in self.network:
                    print(f"[{self.node_id}] ➡️ Forwarding to {next_node_id}")
                    self.network[next_node_id].receive(payload)
                else:
                    print(f"[{self.node_id}] 🚫 Unknown node: {next_node_id}")
            else:
                print(f"[{self.node_id}] 📩 Final message: {decrypted.decode(errors='ignore')}")
        except CryptoError:
            print(f"[{self.node_id}] ❌ Decryption failed: An error occurred trying to decrypt the message")

    def send_to_node(self, node_id, encrypted_payload):
        if node_id in self.network:
            self.network[node_id].receive(encrypted_payload)
        else:
            print(f"[{self.node_id}] 🚫 Unknown node: {node_id}")