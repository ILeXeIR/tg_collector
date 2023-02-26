import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from fastapi import APIRouter

from src.settings import settings
from .handlers import handlers_router


TOKEN = settings.TG_BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
storage=MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(handlers_router)

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