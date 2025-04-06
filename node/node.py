import base64
from network.secure_network import EncryptedChannel, OnionPacket
from nacl.public import PublicKey

class Node:
    def __init__(self, node_id, encrypted_channel: EncryptedChannel):
        self.node_id = node_id
        self.encrypted_channel = encrypted_channel
        self.channel = EncryptedChannel()
        self.network = {}  # populated externally with node_id: Node instance

    def handle_onion_message(self, encrypted_message: bytes):
        try:
            decrypted_data = OnionPacket.unwrap_layer(encrypted_message, self.encrypted_channel.private_key)
            print(f"[{self.node_id}] ✅ Decrypted a layer.")

            if self.is_final_recipient(decrypted_data):
                print(f"[{self.node_id}] 🎯 Final recipient. Message: {decrypted_data.decode()}")
            else:
                next_hop, next_payload = self.extract_next_hop(decrypted_data)
                print(f"[{self.node_id}] ➡️ Forwarding to {next_hop}")
                self.send_to_node(next_hop, next_payload)

        except Exception as e:
            print(f"[{self.node_id}] ❌ Decryption failed: {e}")

    def is_final_recipient(self, decrypted_data: bytes) -> bool:
        return not decrypted_data.startswith(b"HOP:")

    def extract_next_hop(self, decrypted_data: bytes) -> tuple:
        try:
            lines = decrypted_data.split(b"\n", 1)
            next_hop_line = lines[0].decode()
            _, hop_id = next_hop_line.split(":")
            return hop_id, lines[1]
        except Exception:
            raise ValueError("Invalid onion layer format")

    def send_to_node(self, target_id, payload):
        if target_id in self.network:
            print(f"[{self.node_id}] 📤 Sending to {target_id}")
            self.network[target_id].receive(payload)
        else:
            print(f"[{self.node_id}] 🚫 Unknown node: {target_id}")
    
    def receive(self, encrypted_payload):
        try:
            decrypted = OnionPacket.unwrap_layer(self.encrypted_channel.private_key, encrypted_payload)
            if decrypted.startswith(b"HOP:"):
                header, _, rest = decrypted.partition(b"\n")
                next_node = header.decode().split("HOP:")[1].strip()
                print(f"[{self.node_id}] ✅ Decrypted a layer. Forwarding to {next_node}")
                self.send_to_node(next_node, rest)
            else:
                print(f"[{self.node_id}] 💬 Final message: {decrypted.decode()}")
        except Exception as e:
            print(f"[{self.node_id}] ❌ Decryption failed: {e}")
