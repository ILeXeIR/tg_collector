from fastapi import APIRouter, Request, WebSocket
from fastapi.security import OAuth2PasswordBearer


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None,
                        websocket: WebSocket = None):
        return await super().__call__(request or websocket)

oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="users/login")
users_router = APIRouter()
