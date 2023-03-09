import datetime

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    time_delta = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": datetime.datetime.utcnow() + time_delta})
    return jwt.encode(to_encode, settings.SECRET_KEY,
                        algorithm=settings.ALGORITHM)

def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.decode(token, settings.SECRET_KEY,
                                algorithms=settings.ALGORITHM)
    except JWTError:
        return None
    else:
        return encoded_jwt