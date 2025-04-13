# ashans-api/app/utils/wallet_loader.py

import os
import base64
from fastapi import HTTPException
from app.utils.jwt_utils import decode_jwt_token
from wallet.wallet import Wallet  # adjust if your Wallet class path is different
from core.blockchain_instance import DEFAULT_SECRET, WALLETS_DIR


def load_wallet_from_token(token: str) -> Wallet:
    try:
        # Decode the JWT token
        decoded_token = decode_jwt_token(token)
        
        # Ensure decoded_token is a dictionary and contains the expected data
        if not isinstance(decoded_token, dict):
            raise HTTPException(status_code=400, detail="Invalid token format.")
        
        # The address should be in decoded_token['address'] or similar, depending on your JWT structure
        wallet_address = decoded_token.get('address')
        if not wallet_address:
            raise HTTPException(status_code=400, detail="Wallet address not found in token.")
        
        # Load the wallet from the address (or other methods depending on your use case)
        wallet_instance = Wallet.load_wallet_from_address(wallet_address)
        
        return wallet_instance
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Wallet loading failed: {str(e)}")
