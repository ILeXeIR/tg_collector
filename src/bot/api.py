from typing import List

from fastapi import Depends
from pydantic import parse_obj_as

from src.users.models import UserRp
from src.users.services import get_current_user
from .dao import ActiveChat, CustomStorage
from .deps import bot_router
from .models import StateRp
from .services import send_from_bot


@bot_router.get("/active_chats")
async def get_active_chats(
        current_user: UserRp = Depends(get_current_user)) -> List[int]:
    return await ActiveChat.all().order_by("chat_id").values_list("chat_id", 
                                                                  flat=True)


@bot_router.post("/chat/{chat_id}")
async def send_in_chat(chat_id: int, text: str,
                       current_user: UserRp = Depends(get_current_user)) -> str:
    return await send_from_bot(chat_id=chat_id, text=text)


@bot_router.get("/chat_states/{chat_id}")
async def get_chat_states(
        chat_id: int, current_user: UserRp = Depends(get_current_user)
) -> List[StateRp]:
    states = await CustomStorage.filter(chat_id=chat_id).order_by("user_id")
    return parse_obj_as(List[StateRp], states)


@bot_router.get("/all_states")
async def get_all_states(
        current_user: UserRp = Depends(get_current_user)) -> List[StateRp]:
    states = await CustomStorage.all().order_by("chat_id", "user_id")
    return parse_obj_as(List[StateRp], states)
