from fastapi import APIRouter

from .utils import ConnectionManager


ws_router = APIRouter()
manager = ConnectionManager()