from datetime import datetime
# import json
import logging
# import os
# from pathlib import Path

from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, ChatMemberUpdated
from aiogram.types.message import ContentType
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, \
                                                JOIN_TRANSITION
import asyncio
from fastapi import APIRouter
# import jsonpickle
import requests

from src import settings 
from . import collector, fsm


TOKEN = settings.TG_BOT_TOKEN
API_URL = settings.TG_BOT_API_URL

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(fsm.router)
dp.include_router(collector.router)

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
    webhook = await bot.get_webhook_info()
    print("WEBHOOK_INFO: ", webhook)

@bot_router.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm SpanBot!\n"
                        + "I can save your messages in db.\n"
                        + "You may check api connection with command /check"
                        + " or /rate this bot.")

@dp.message(Command(commands=["check"]))
async def check_api_connection(message: types.Message):
    response = requests.get(API_URL)
    await message.answer(str(response.json()))

@dp.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION)
)
async def bot_was_added_in_chat(event: ChatMemberUpdated):
    chat_id = event.chat.id 
    await bot.send_message(chat_id=chat_id, text="Alloha!")

async def send_message_from_bot(chat_id: int, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return "Done!"
    except Exception:
        return "I can't do that."


async def run_bot():
    # executor.start_polling(dp, skip_updates=True)
    try:
        await bot.set_my_commands(commands, BotCommandScopeDefault())
        await dp.start_polling(bot)
    finally:
        bot.session.close()









