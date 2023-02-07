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

@messages_router.get("/chats", response_model=List[int])
async def get_list_of_chats():
	data = await Messages.all().distinct().values("chat_id")
	list_of_chats = [x["chat_id"] for x in data]
	return list_of_chats

@messages_router.get("/chat_objects/{chat_id}", response_model=List[MessageOUT_Pydantic])
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