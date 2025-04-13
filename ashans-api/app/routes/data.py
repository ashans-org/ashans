# api/endpoints/store.py
import json
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import StoreDataRequest, StoreDataResponse
from core.blockchain_instance import load_blockchain, save_blockchain
from node.node import Node
from utils.block_cost_calculation import calculate_ashans_value
from utils.auth_utils import generate_floating_address
from utils.block_utils import sanitize_block
from app.utils.wallet_loader import load_wallet_from_token  # new
from app.utils.jwt_utils import get_token_from_header  # new

router = APIRouter()

@router.post("/store", response_model=StoreDataResponse)
def store_data(request: StoreDataRequest, token: str = Depends(get_token_from_header)):
    """
    Stores encrypted data in the blockchain and returns success message.
    """
    try:
        # Load wallet instance from the token
        wallet_instance = load_wallet_from_token(token)
        if not wallet_instance:
            raise HTTPException(status_code=400, detail="Invalid token. Wallet could not be loaded.")
        
        # Prepare blockchain and node
        validators = [wallet_instance.get_public_key_pem()]
        blockchain = load_blockchain(validators)
        if wallet_instance.get_public_key_pem() not in blockchain.consensus.validators:
            blockchain.consensus.validators.append(wallet_instance.get_public_key_pem())

        node = Node(wallet=wallet_instance, blockchain=blockchain)

        # Generate floating address based on public key
        pub_key_pem = wallet_instance.get_public_key_pem()
        floating_address = generate_floating_address(pub_key_pem)

        # Encrypt data
        data_dict = {"payload": request.data}
        encrypted_data = wallet_instance.encrypt_data(data_dict, wallet_instance.get_address())

        # Prepare transactions and calculate the Ashans value
        json_data = json.dumps(data_dict).encode()
        ashans_coin, size_mb = calculate_ashans_value(json_data)
        transactions = [{
            "sender": "network",
            "recipient": wallet_instance.get_address(),
            "ashans_coin": ashans_coin,
            "data": encrypted_data
        }]

        # Create and add block to blockchain
        block, proof = node.create_block(transactions)
        if block in blockchain.chain:
            save_blockchain()
            return {"message": "Block mined and added to the blockchain.", "block": sanitize_block(block)}
        else:
            raise HTTPException(status_code=500, detail="Block was not added. Check validator and consensus logic.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))