import argparse
import time
from node.node import Node
from wallet.wallet import Wallet

def simulate_node_startup():
    print("🚀 Starting Ashans Node...")

    wallet = Wallet()
    node = Node(node_id="node_1", wallet=wallet)
    node.start()

    print("✅ Node running with wallet address:", wallet.get_address())
    print("🔄 Simulating basic blockchain interaction...")

    time.sleep(2)
    node.create_block(transactions=["Tx1", "Tx2"])
    node.create_block(transactions=["Tx3"])

    print("📦 Current Blockchain State:")
    for block in node.blockchain.chain:
        print(f" - Block #{block.index} | Hash: {block.hash[:10]}...")

    print("🛑 Node simulation complete.")

def main():
    parser = argparse.ArgumentParser(description="Ashans Full Node Simulation")
    parser.add_argument("--simulate", action="store_true", help="Run a node simulation")
    args = parser.parse_args()

    if args.simulate:
        simulate_node_startup()
    else:
        print("ℹ️ Use --simulate to run the node simulation demo.")

if __name__ == "__main__":
    main()