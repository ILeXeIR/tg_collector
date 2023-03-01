from fastapi import APIRouter

from .utils import CustomOAuth2PasswordBearer


oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="users/login")
users_router = APIRouter()
