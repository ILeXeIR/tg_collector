import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from fastapi import APIRouter
from typing import List

from src import settings
from .dao import ActiveChats
from . import handlers


TOKEN = settings.TG_BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(handlers.router)

bot_router = APIRouter()

commands = [
    BotCommand(
        command="start",
        description="Bot description"
    ),
    BotCommand(
        command="help",
        description="Help"
    ),
    BotCommand(
        command="check",
        description="Check connection to DB"
    ),
    BotCommand(
        command="rate",
        description="Rate this bot"
    ),
    BotCommand(
        command="cancel",
        description="Exit from FSM"
    )
]

@bot_router.on_event("startup")
async def on_startup():
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await bot.set_webhook(url=settings.WEBHOOK_URL, drop_pending_updates=True)

    # Get current webhook status
    # webhook = await bot.get_webhook_info()
    # print("WEBHOOK_INFO: ", webhook)

@bot_router.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@bot_router.get("/active_chats", response_model=List[int])
async def get_active_chats():
    return await ActiveChats.all().order_by("chat_id").values_list("chat_id", 
                                                                    flat=True)

@bot_router.post("/chat/{chat_id}")
async def send_from_bot(chat_id: int, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return "Done!"
    except Exception:
        return "I can't do that."









