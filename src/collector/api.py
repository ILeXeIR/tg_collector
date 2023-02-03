import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .dao import Messages
from .models import Message_Pydantic

messages_router = APIRouter()

@messages_router.get("/", response_model=List[Message_Pydantic])
async def get_messages():
	return await Messages.all()

@messages_router.post("/")
async def create_message(data: dict):
	message = Message_Pydantic(
    	message_id=data['message_id'],
    	chat_id=data['chat_id'],
    	dispatch_time=data['datetime'],
    	sender=data['sender'],
    	message_type=data['type'],
    	text=data['text']
	)
	message.id = str(message.chat_id) + "-" + str(message.message_id)
	await Messages.create(**message.dict())
