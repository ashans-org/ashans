
import time
import hashlib
import os

class FloatingTokenAddress:
    def __init__(self, master_seed):
        self.master_seed = master_seed.encode()

    def generate_address(self, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        interval = timestamp // 10  # New address every 10 seconds
        base_hash = hashlib.sha256(self.master_seed + str(interval).encode()).hexdigest()
        return self._distribute_parts(base_hash)

    def _distribute_parts(self, address_hash):
        # Split address hash into 4 parts for distributed node sharing
        part_size = len(address_hash) // 4
        parts = [address_hash[i:i+part_size] for i in range(0, len(address_hash), part_size)]
        return parts

# Simulated usage
if __name__ == "__main__":
    seed = "ashans_secure_seed"
    addr_gen = FloatingTokenAddress(seed)

    current_parts = addr_gen.generate_address()
    print("Floating token address (parts):")
    for i, part in enumerate(current_parts):
        print(f"Part {i+1}: {part}")
