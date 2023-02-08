from datetime import datetime
#import json
import logging
#import os
#from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType
#import jsonpickle
import requests

from src import settings 
from . import fsm


TOKEN = settings.TG_BOT_TOKEN
API_URL = "http://127.0.0.1:8000/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

fsm.register_handler_fsm(dp)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm SpanBot!\n"
                        + "I can save your messages in db.\n"
                        + "You may check api connection with command /check"
                        + " or /rate this bot.")

@dp.message_handler(commands=["check"])
async def check_api_connection(message: types.Message):
    response = requests.get(API_URL)
    await message.reply(response.json())

@dp.message_handler(content_types=ContentType.ANY)
async def send_message(message: types.Message):
    data = dict(message)
    data["content_type"] = message.content_type
    response = requests.post(f"{API_URL}messages", json=data)
    #await message.reply(response.status_code)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

def run_bot():
    executor.start_polling(dp, skip_updates=True)

"""
@dp.message_handler()
async def save_text_message(message: types.Message):
    chat_id = message.chat.id
    date_time = message.date
    filename = str(message.message_id) + '.json'
    filepath = Path('downloads', str(chat_id), filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.touch()
    data = {
        "message_id": message.message_id,
        "chat_id": message.chat.id,
        "datetime": date_time.strftime("%d.%m.%Y %H:%M:%S"),
        "sender": message.from_user.username,
        "type": message.content_type,
        "text": message.text
    }
    with open(filepath, 'w') as file_object:
        #text = message.from_user.username + ":\n" + message.text
        #message_json = jsonpickle.encode(message, indent=2)
        #file_object.write(message_json)
        json.dump(data, file_object, indent=2)
    await bot.send_document(chat_id=chat_id, document=types.InputFile(filepath))

@dp.message_handler(content_types=ContentType.PHOTO)
async def save_image(message: types.Message):
    chat_id = message.chat.id
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path
    filepath = Path('downloads', str(chat_id), filename)
    file = await bot.download_file(filename, filepath)
    await bot.send_document(chat_id=chat_id, document=types.InputFile(filepath))
    await save_text_message(message, m_type="image", m_text=message.caption)

    filename2 = str(message.message_id) + '.json'
    filepath2 = Path('downloads', str(chat_id), filename2)
    filepath2.touch()
    with open(filepath2, 'w') as file_object:
        message_json = jsonpickle.encode(message, indent=2)
        file_object.write(message_json)
    await bot.send_document(chat_id=chat_id, document=types.InputFile(filepath2))
"""








