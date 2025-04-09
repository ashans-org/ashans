from datetime import datetime, timedelta
from jose import jwt
from app.settings import SECRET_KEY, ALGORITHM

def create_jwt_token(data, expires_delta: timedelta = timedelta(minutes=30)):
    if not isinstance(data, dict):
        raise ValueError("Expected data to be a dictionary")

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
