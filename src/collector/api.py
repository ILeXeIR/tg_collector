from fastapi import Depends, Request
from pydantic import parse_obj_as
from typing import List

from src.settings import settings
from src.users.models import UserRp
from src.users.services import get_current_user
from .dao import Message
from .deps import messages_router
from .models import MessageRp
from .services import handle_message


@messages_router.get("/")
async def get_messages(
        current_user: UserRp = Depends(get_current_user)) -> List[MessageRp]:
    messages = await Message.all()
    return parse_obj_as(List[MessageRp], messages)


@messages_router.post("/")
async def save_message(update: Request):
    webhook_token = update.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if webhook_token == settings.WEBHOOK_TOKEN:
        await handle_message(update=update)


@messages_router.get("/chats")
async def get_list_of_chats(
        current_user: UserRp = Depends(get_current_user)) -> List[int]:
    list_of_chats = Message.exclude(chat_id=None).order_by("chat_id")
    list_of_chats = list_of_chats.distinct().values_list("chat_id", flat=True)
    return await list_of_chats


@messages_router.get("/chat_objects/{chat_id}")
async def get_chat_messages(
        chat_id: int, current_user: UserRp = Depends(get_current_user)
) -> List[MessageRp]:
    messages = await Message.filter(chat_id=chat_id)
    return parse_obj_as(List[MessageRp], messages)
