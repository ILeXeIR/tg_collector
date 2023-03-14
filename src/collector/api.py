from fastapi import Depends, Request
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
    return [MessageRp.from_orm(x) for x in messages]


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
    return await Message.filter(chat_id=chat_id)


@messages_router.get("/chat/{chat_id}")
async def show_chat(
        chat_id: int, current_user: UserRp = Depends(get_current_user)
    ) -> List[str]:
    data = await Message.filter(chat_id=chat_id)
    chat = []
    for d in data:
        message = f"{d.sender} ({d.dispatch_time})"
        if d.message_type != "text":
            message += f"\nSent {d.message_type}"
            if d.text:
                message += f" with text:\n'{d.text}'"
        else:
            message += f":\n'{d.text}'"
        chat.append(message)
    return chat
