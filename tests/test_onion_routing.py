import base64
from network.secure_network import EncryptedChannel, OnionPacket
from nacl.public import PrivateKey

def base64_key(key_obj):
    return base64.b64encode(key_obj.encode()).decode()

def test_onion_routing():
    # Create 3 nodes (each with private/public keys)
    node_keys = [PrivateKey.generate() for _ in range(3)]
    public_keys_b64 = [base64_key(k.public_key) for k in node_keys]

    # Original message to send
    message = b"secret message to final node"

    # Build and wrap the onion packet
    packet = OnionPacket(message, path=public_keys_b64)
    encrypted_packet = packet.wrap_layers()

    # Each node unwraps one layer
    current_packet = encrypted_packet
    for i, priv_key in enumerate(node_keys):
        print(f"Node {i+1} decrypting...")
        current_packet = OnionPacket.unwrap_layer(current_packet, priv_key)

    assert current_packet == message
    print("✅ Final message decrypted successfully.")
