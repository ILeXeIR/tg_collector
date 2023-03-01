from fastapi import Depends

from src.users.models import UserRp
from src.users.services import get_current_user
from .deps import bot


async def send_from_bot(
        chat_id: int, text: str,
        current_user: UserRp = Depends(get_current_user)
    ) -> str:
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return "Done!"
    except Exception as e:
        return e