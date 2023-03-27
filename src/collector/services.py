from datetime import datetime
import json

from aiogram import types
from fastapi import Request

from src.bot.deps import bot, dp
from src.websocket.deps import manager
from .dao import Message
from .models import MessageRq


async def handle_message(update: Request):
    # Save message in DB, send to bot Dispatcher and to WebSocket manager

    update_json = await update.json()
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
        sender_id=data.get("from", dict()).get("id"),
        message_type=data.get("content_type"),
        text=text,
        attachment=update_json
    )
    message = await Message.create(**message_for_db.dict())
    await dp.feed_update(bot, update=update)
    if chat_id is not None:
        await manager.broadcast(message=message, chat_id=chat_id)
