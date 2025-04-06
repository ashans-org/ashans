import threading
import time
from network.encryption import EncryptedChannel
from nacl.public import PrivateKey

def simulate_node(sender_private, receiver_private, message_to_send, result_dict, key):
    sender_public = sender_private.public_key
    receiver_public = receiver_private.public_key

    sender_channel = EncryptedChannel(private_key=sender_private, peer_public_key=receiver_public)
    receiver_channel = EncryptedChannel(private_key=receiver_private, peer_public_key=sender_public)

    encrypted_message = sender_channel.encrypt(message_to_send.encode())
    decrypted_message = receiver_channel.decrypt(encrypted_message).decode()

    result_dict[key] = decrypted_message

def test_node_to_node_communication():
    sender_private = PrivateKey.generate()
    receiver_private = PrivateKey.generate()

    shared_data = {}

    thread = threading.Thread(
        target=simulate_node,
        args=(sender_private, receiver_private, "Node-to-node secure message", shared_data, "msg")
    )
    thread.start()
    thread.join()

    assert shared_data["msg"] == "Node-to-node secure message"