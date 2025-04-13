from datetime import datetime, timedelta
from jose import jwt
from app.settings import SECRET_KEY, ALGORITHM
from fastapi import Header, HTTPException
from typing import Optional
from jwt import PyJWTError 

def create_jwt_token(data, expires_delta: timedelta = timedelta(minutes=30)):
    if not isinstance(data, dict):
        raise ValueError("Expected data to be a dictionary")

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

def get_token_from_header(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization token missing or malformed.")
    token = authorization[7:]  # Extract the token from 'Bearer <token>'
    return token