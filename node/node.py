from core.blockchain import Blockchain
import time
from network.encryption import EncryptedChannel
from wallet.wallet import Wallet
from consensus.poa import ProofOfAuthority

class Node:
    def __init__(self, node_id=None, wallet=None, blockchain=None):
        self.node_id = node_id
        self.wallet = wallet if wallet else Wallet()

        if blockchain:
            self.blockchain = blockchain
        else:
            consensus = ProofOfAuthority(validators=[self.wallet.get_public_key_pem()])
            self.blockchain = Blockchain(consensus=consensus)

        self.peers = {}  # peer_id -> EncryptedChannel
        self.running = False
        self.pending_transactions = []

    def create_block(self, transactions):
        from core.block import Block

        validator = self.wallet.get_public_key_pem()
        reward_tx = {
            "from": "network",
            "to": self.wallet.get_address(),
            "amount": 10
        }

        transactions.append(reward_tx)

        block = Block(
            index=len(self.blockchain.chain),
            previous_hash=self.blockchain.get_last_block().hash,
            transactions=transactions,
            validator=validator,
            consensus=str(type(self.blockchain.consensus))
        )

        proof = self.blockchain.consensus.get_proof(validator)
        success = self.blockchain.add_block(block, proof)
        if success:
            print(f"✅ New block created. Address {self.wallet.get_address()} received 10 coins.")
        else:
            print("❌ Failed to add block to chain.")

        self.pending_transactions = []
        return block, proof

    def add_peer(self, peer_id, peer_public_key):
        channel = EncryptedChannel(self.wallet.get_private_key(), peer_public_key)
        self.peers[peer_id] = channel

    def send_message(self, peer_id, message):
        if peer_id in self.peers:
            encrypted = self.peers[peer_id].encrypt(message.encode())
            print(f"[{self.node_id}] Sending encrypted message to {peer_id}: {encrypted}")
            return encrypted
        else:
            print(f"[{self.node_id}] No such peer: {peer_id}")
            return None

    def receive_message(self, peer_id, encrypted_message):
        if peer_id in self.peers:
            try:
                decrypted = self.peers[peer_id].decrypt(encrypted_message).decode()
                print(f"[{self.node_id}] Received message from {peer_id}: {decrypted}")
                return decrypted
            except Exception as e:
                print(f"[{self.node_id}] Failed to decrypt message: {e}")
        else:
            print(f"[{self.node_id}] No such peer: {peer_id}")
            return None

    def run(self):
        self.running = True
        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False

    def start(self):
        print(f"🔗 Node {self.node_id} is starting...")
        print(f"🧠 Wallet Public Key: {self.wallet.get_public_key_pem()}")
