from datetime import datetime
import json

from aiogram import Router, types

from src import settings
from src.collector.dao import Messages
from src.collector.models import Message_Pydantic


router = Router()

@router.message()
async def save_message(message: types.Message, update_json: dict):
    #Save message in DB
    
    data = update_json["message"]
    data["date"] = datetime.fromtimestamp(data["date"])
    data["date"] = data["date"].strftime("%d.%m.%Y %H:%M:%S")
    data["content_type"] = message.content_type
    if data.get('text'):
        text = data['text']
    elif data.get('caption'):
        text = data['caption']
    else:
        text = ""
    message_json = json.dumps(data, indent=2)
    message_for_db = Message_Pydantic(
        message_id=data['message_id'],
        chat_id=data['chat']['id'],
        dispatch_time=data["date"],
        sender=data['from']['username'],
        message_type=data["content_type"],
        text=text,
        attachment=message_json
    )
    message_for_db.id = update_json['update_id']
    await Messages.create(**message_for_db.dict())
    # await message.reply("OK")


