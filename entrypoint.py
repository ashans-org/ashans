
from core.blockchain import Blockchain
from consensus.poa import PoAValidator

if __name__ == "__main__":
    print("🔗 Welcome to the Ashans Blockchain Node")
    blockchain = Blockchain()
    poa = PoAValidator()

    # Simple startup message
    print("🚀 Node initialized with empty blockchain and PoA validator.")
