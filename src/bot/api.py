from typing import List

from .dao import ActiveChat
from .deps import bot, bot_router


@bot_router.get("/active_chats")
async def get_active_chats() -> List[int]:
    return await ActiveChat.all().order_by("chat_id").values_list("chat_id", 
                                                                    flat=True)

@bot_router.post("/chat/{chat_id}")
async def send_from_bot(chat_id: int, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return "Done!"
    except Exception as e:
        return e

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





