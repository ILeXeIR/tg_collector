from fastapi import Depends, HTTPException, status

from .dao import User
from .deps import oauth2_scheme
from .models import UserRp
from .security import decode_access_token


async def get_current_user(
        token: str = Depends(oauth2_scheme)) -> UserRp:
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
    current_user = await User.get_or_none(username=username)
    if current_user is None:
        raise cred_exception
    return UserRp.from_orm(current_user)
