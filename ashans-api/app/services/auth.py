from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from app.settings import SECRET_KEY, ALGORITHM


def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")