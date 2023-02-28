from typing import List

from aiogram.fsm.storage.base import StorageKey
from fastapi import Depends

from src.collector.dao import Message
from src.users.models import UserRp
from src.users.services import get_current_user
from .dao import ActiveChat
from .deps import bot, bot_router, storage


@bot_router.get("/active_chats")
async def get_active_chats(
        current_user: UserRp = Depends(get_current_user)) -> List[int]:
    return await ActiveChat.all().order_by("chat_id").values_list("chat_id", 
                                                                    flat=True)

@bot_router.post("/chat/{chat_id}")
async def send_from_bot(
        chat_id: int, text: str,
        current_user: UserRp = Depends(get_current_user)
    ) -> str:
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return "Done!"
    except Exception as e:
        return e

@bot_router.get("/users")
async def get_users(
        chat_id: int, current_user: UserRp = Depends(get_current_user)
    ) -> List[int]:
    users_list = Message.filter(chat_id=chat_id).order_by("sender_id")
    users_list = users_list.distinct().values_list("sender_id", flat=True)
    return await users_list

@bot_router.get("/state")
async def get_states(
        chat_id: int, current_user: UserRp = Depends(get_current_user)
    ) -> dict:
    users_list = await get_users(chat_id)
    users_states = {}
    for user_id in users_list:
        key = StorageKey(bot_id=bot.id, chat_id=chat_id, user_id=user_id)
        state = await storage.get_state(bot=bot, key=key)
        if state is not None:
            users_states[user_id] = state
    return users_states

"""
@bot_router.get("/get_chat/{chat_id}")
async def get_chat(chat_id: int):
    return await bot.get_chat(chat_id)

@bot_router.get("/get_chat_member/")
async def get_chat_member(chat_id: int, user_id: int):
    return await bot.get_chat_member(chat_id, user_id)

@bot_router.get("/get_chat_member_count/{chat_id}")
async def get_chat_member_count(chat_id: int):
    return await bot.get_chat_member_count(chat_id)

@bot_router.get("/get_chat_administrators/{chat_id}")
async def get_chat_administrators(chat_id: int):
    return await bot.get_chat_administrators(chat_id)

@bot_router.get("/get_current_state/")
async def get_current_state(chat_id: int, user_id: int):
    return await dp.current_state(chat_id=chat_id, user_id=user_id)
"""





