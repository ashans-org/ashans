from node.node import Node
from network.secure_network import EncryptedChannel, OnionPacket
from nacl.public import PrivateKey

# ✅ Define create_node
def create_node(name):
    node = Node(name)
    node.channel = EncryptedChannel()  # each node has its own channel (private/public key)
    return node
def simulate_onion_routing():
    nodeA = create_node("NodeA")
    nodeB = create_node("NodeB")
    nodeC = create_node("NodeC")

    # Each node has a network dict so it knows its neighbors
    nodeA.network = {"NodeB": nodeB}
    nodeB.network = {"NodeC": nodeC}
    nodeC.network = {}

    final_message = b"Secret message for NodeC"

    # Build routing path from final to first (reverse order)
    routing_path = [
        ("NodeC", nodeC.channel.public_key),
        ("NodeB", nodeB.channel.public_key),
    ]

    # Encrypt in reverse (inner layer first)
    sender_channel = nodeA.channel  # use consistent sender
    payload = final_message

    for node_id, pubkey in reversed(routing_path):
        print(f"[Debug] Wrapping layer for {node_id}")
        layer = f"HOP:{node_id}\n".encode() + payload
        payload = sender_channel.encrypt(pubkey, layer)  # use nodeA’s key
    print("\n🚀 Onion Routing Simulation Started\n")
    nodeA.send_to_node("NodeB", payload)

# Run the simulation
simulate_onion_routing()