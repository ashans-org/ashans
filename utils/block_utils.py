def sanitize_block(block):
    """
    Returns a dict version of the block with only serializable fields.
    Ensures all block data is JSON-serializable and suitable for hashing or export.
    """
    return {
        "index": block.index,
        "timestamp": block.timestamp,
        "transactions": block.transactions,
        "previous_hash": block.previous_hash,
        "nonce": block.nonce,
        "validator": block.validator,
        "hash": block.hash if hasattr(block, "hash") else None
    }
