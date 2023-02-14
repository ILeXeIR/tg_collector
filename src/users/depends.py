from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.security import decode_access_token
from .dao import Users
from .models import User_Pydantic


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_current_user(
        token: str = Depends(oauth2_scheme)) -> User_Pydantic:
    cred_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    username: str = payload.get("sub")
    if username is None:
        raise cred_exception
    current_user = await Users.get_or_none(username=username)
    if current_user is None:
        raise cred_exception
    return current_user
