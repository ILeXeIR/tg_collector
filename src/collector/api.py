from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .dao import Messages
from .models import Message_Pydantic, MessageOUT_Pydantic

messages_router = APIRouter()

@messages_router.get("/", response_model=List[MessageOUT_Pydantic])
async def get_messages():
	return await Messages.all()

@messages_router.post("/")
async def create_message(data: dict):
	if data.get('text'):
		text = data['text']
	elif data.get('caption'):
		text = data['caption']
	else:
		text = ""
	date_time = datetime.fromtimestamp(data['date'])
	message_json = json.dumps(data, indent=2)
	message = Message_Pydantic(
    	message_id=data['message_id'],
    	chat_id=data['chat']['id'],
    	dispatch_time=date_time.strftime("%d.%m.%Y %H:%M:%S"),
    	sender=data['from']['username'],
    	message_type=data['content_type'],
    	text=text,
    	attachment=message_json
	)
	message.id = str(message.chat_id) + "-" + str(message.message_id)
	await Messages.create(**message.dict())
