from .deps import bot


async def send_from_bot(chat_id: int, text: str) -> str:
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return "Done!"
    except Exception as e:
        return e