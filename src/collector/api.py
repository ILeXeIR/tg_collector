from datetime import datetime
import json

from aiogram import types
from fastapi import Request
from typing import List

from src.bot.deps import bot, dp
from src.websocket.deps import manager
from .dao import Message
from .deps import messages_router
from .models import MessageRq, MessageRp


@messages_router.get("/")
async def get_messages() -> List[MessageRp]:
    return await Message.all()

@messages_router.post("/")
async def create_message(update: Request):
    # Save message in DB and send to bot Dispatcher
    update_json = await update.json()
    # print("UPDATE_JSON: ", update_json)
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
    update_json = json.dumps(update_json, indent=2)
    if data.get("text"):
        text = data["text"]
    elif data.get("caption"):
        text = data["caption"]
    else:
        text = ""
    chat_id = data.get("chat", dict()).get("id")
    message_for_db = MessageRq(
        message_id=data.get("message_id"),
        chat_id=chat_id,
        dispatch_time=data.get("date"),
        sender=data.get("from", dict()).get("username"),
        message_type=data.get("content_type"),
        text=text,
        attachment=update_json
    )
    message = await Message.create(**message_for_db.dict())
    await dp.feed_update(bot, update=update)
    if chat_id is not None:
        await manager.broadcast(message=message, chat_id=chat_id)

@messages_router.get("/chats")
async def get_list_of_chats() -> List[int]:
    list_of_chats = await Message.all().distinct().values_list("chat_id",
                                                                flat=True)
    return sorted(list_of_chats)

@messages_router.get("/chat_objects/{chat_id}")
async def get_chat_messages(chat_id: int) -> List[MessageRp]:
    return await Message.filter(chat_id=chat_id)

@messages_router.get("/chat/{chat_id}")
async def show_chat(chat_id: int) -> List[str]:
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