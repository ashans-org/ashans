from node.node import Node
from network.secure_network import EncryptedChannel, OnionPacket
from nacl.public import PrivateKey

def create_node(node_id):
    private_key = PrivateKey.generate()
    channel = EncryptedChannel(private_key=private_key)
    return Node(node_id, channel)


def simulate_onion_routing():
    nodeA = create_node("NodeA")
    nodeB = create_node("NodeB")
    nodeC = create_node("NodeC")

    # Define reachable nodes
    nodeA.network = {"NodeB": nodeB}
    nodeB.network = {"NodeC": nodeC}
    nodeC.network = {}
    final_message = b" Secret message for NodeC"

    # Important: build onion from inner (NodeC) to outer (NodeB)
    routing_path = [
        ("NodeC", nodeC.encrypted_channel.public_key),  # Final hop
        ("NodeB", nodeB.encrypted_channel.public_key),  # First hop
    ]

    payload = final_message
    for node_id, pubkey in reversed(routing_path):
        # Wrap each layer in HOP header and encrypt
        layer = f"HOP:{node_id}\n".encode() + payload
        onion = OnionPacket(layer, [])
        payload = onion.encrypt_layer(pubkey, nodeA.encrypted_channel.private_key)

    print("\n🚀 Onion Routing Simulation Started\n")
    # Send initial message to NodeB (not NodeA)
    nodeA.send_to_node("NodeB", payload)


if __name__ == "__main__":
    simulate_onion_routing()
