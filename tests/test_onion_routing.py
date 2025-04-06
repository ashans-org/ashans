from network.secure_network import EncryptedChannel, OnionPacket
from nacl.public import PrivateKey
import base64

def test_onion_message_decryption_chain():
    # Setup 3 nodes with key pairs
    nodes = [PrivateKey.generate() for _ in range(3)]
    public_keys_b64 = [base64.b64encode(n.public_key.encode()).decode() for n in nodes]

    # Original payload
    original_message = b"Secret payload for Node C"

    # Create onion packet (Node A → Node B → Node C)
    onion = OnionPacket(original_message, path=public_keys_b64)
    layered_packet = onion.wrap_layers()

    # Now unwrap layer-by-layer
    current_data = layered_packet
    for priv_key in nodes:
        current_data = OnionPacket.unwrap_layer(current_data, priv_key)

    assert current_data == original_message
    print("✅ Onion routing simulation passed. Final decrypted message:", current_data.decode())
