class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.channel = EncryptedChannel()
        self.private_key = self.channel.private_key
        self.network = {}

    def send_to_node(self, target_id, payload):
        if target_id not in self.network:
            print(f"[{self.node_id}] 🚫 Unknown node: {target_id}")
            return
        next_node = self.network[target_id]
        next_node.receive(payload)

    def receive(self, encrypted_payload: bytes):
        print(f"[{self.node_id}] Received packet")
        decrypted = OnionPacket.unwrap_layer(self.private_key, encrypted_payload)
        if decrypted is None:
            print(f"[{self.node_id}] ❌ Decryption failed: An error occurred trying to decrypt the message")
            return

        if decrypted.startswith(b"HOP:"):
            header, rest = decrypted.split(b"\n", 1)
            _, next_hop = header.decode().split(":")
            print(f"[{self.node_id}]  Decrypted a layer. ➡️ Forwarding to {next_hop}")
            self.send_to_node(next_hop, rest)
        else:
            print(f"[{self.node_id}]  Final decrypted message: {decrypted.decode()}")