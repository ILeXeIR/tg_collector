from aiogram import types
from fastapi import APIRouter, Request
from typing import List

from src.bot.bot import send_message_from_bot, bot, dp
from .dao import Messages
from .models import MessageOUT_Pydantic


messages_router = APIRouter()

@messages_router.get("/", response_model=List[MessageOUT_Pydantic])
async def get_messages():
    return await Messages.all()

@messages_router.post("/")
async def create_message(update: Request):
    update_json = await update.json()
    await dp.feed_update(bot, update=types.Update(**update_json), 
                        update_json=update_json)

@messages_router.get("/chats", response_model=List[int])
async def get_list_of_chats():
    data = await Messages.all().distinct().values("chat_id")
    list_of_chats = sorted([x["chat_id"] for x in data])
    return list_of_chats

@messages_router.get("/chat_objects/{chat_id}",
                    response_model=List[MessageOUT_Pydantic])
async def get_chat_messages(chat_id: int):
    return await Messages.filter(chat_id=chat_id)

@messages_router.get("/chat/{chat_id}", response_model=List[str])
async def show_chat(chat_id: int):
    data = await Messages.filter(chat_id=chat_id)
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

@messages_router.post("/chat/{chat_id}")
async def send_from_bot(chat_id: int, text: str):
    answer = await send_message_from_bot(chat_id, text)
    return answer