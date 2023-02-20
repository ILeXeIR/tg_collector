from datetime import datetime
import json

from aiogram import types
from fastapi import APIRouter, Request
from typing import List

from src.bot.bot import send_message_from_bot, bot, dp
from .dao import Messages
from .models import Message_Pydantic, MessageOUT_Pydantic


messages_router = APIRouter()

@messages_router.get("/", response_model=List[MessageOUT_Pydantic])
async def get_messages():
    return await Messages.all()

@messages_router.post("/")
async def create_message(update: Request):
    # Save message in DB and send to bot Dispatcher
    update_json = await update.json()
    print("UPDATE_JSON: ", update_json)
    update = types.Update(**update_json)
    for key in update_json:
        if key != "update_id":
            data = update_json[key]
            if key == "message":
                data["content_type"] = "message_" + update.message.content_type
            else:
                data["content_type"] = key
            break
    if data.get("date"):
        data["date"] = datetime.fromtimestamp(data["date"])
        data["date"] = data["date"].strftime("%d.%m.%Y %H:%M:%S")
    id = str(update_json["update_id"])
    update_json = json.dumps(update_json, indent=2)
    if data.get("text"):
        text = data["text"]
    elif data.get("caption"):
        text = data["caption"]
    else:
        text = ""
    message_for_db = Message_Pydantic(
        id=id,
        message_id=data.get("message_id"),
        chat_id=data.get("chat", dict()).get("id"),
        dispatch_time=data.get("date"),
        sender=data.get("from", dict()).get("username"),
        message_type=data.get("content_type"),
        text=text,
        attachment=update_json
    )
    await Messages.create(**message_for_db.dict())
    await dp.feed_update(bot, update=update)

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