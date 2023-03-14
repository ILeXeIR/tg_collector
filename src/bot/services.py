from .deps import bot


async def send_from_bot(chat_id: int, text: str) -> str:
    if not text.strip():
        return "Message can't be empty."
    await bot.send_message(chat_id=chat_id, text=text)
    return "Done!"
