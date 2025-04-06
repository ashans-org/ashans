from nacl.public import PrivateKey
from network.encryption import EncryptedChannel

def test_encryption_and_decryption():
    # Generate key pairs for both parties
    sender_private = PrivateKey.generate()
    receiver_private = PrivateKey.generate()

    sender_public = sender_private.public_key
    receiver_public = receiver_private.public_key

    # Sender encrypts using receiver's public key
    sender_channel = EncryptedChannel(private_key=sender_private, peer_public_key=receiver_public)
    message = b"secret message"
    encrypted = sender_channel.encrypt(message)

    # Receiver decrypts using sender's public key
    receiver_channel = EncryptedChannel(private_key=receiver_private, peer_public_key=sender_public)
    decrypted = receiver_channel.decrypt(encrypted)

    assert decrypted == message