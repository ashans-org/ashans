
from consensus.poa import PoAValidator

# Simulate 3 authority nodes
poa = PoAValidator()
node_A = poa.register_node("node_A", "secretA")
node_B = poa.register_node("node_B", "secretB")
node_C = poa.register_node("node_C", "secretC")

# Node A creates a block and signs it
block_data = "{ 'index': 1, 'data': 'Sample Transaction' }"
signature = node_A.sign_block(block_data)

# Broadcast to other nodes (simulation)
print("Node A signed block data.")

# Node B validates the block
valid_B = poa.validate_block("node_A", block_data, signature)
print(f"Node B validation result: {valid_B}")

# Node C validates the block
valid_C = poa.validate_block("node_A", block_data, signature)
print(f"Node C validation result: {valid_C}")
