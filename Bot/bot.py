import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()  # take environment variables from .env.

TOKEN = os.environ.get('TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm SpanBot!\n"
                        + "I can save your text and photo messages as files.")

@dp.message_handler()
async def save_text_message(message: types.Message):
    chat_id = message.chat.id
    filename = str(datetime.now())[:19] + '.txt'
    filename = filename.replace('-', '_').replace(':', '_').replace(' ', '_')
    filepath = Path('downloads', str(chat_id), filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.touch()
    with open(filepath, 'w') as file_object:
        text = message.from_user.username + ":\n" + message.text
        file_object.write(text)
    await bot.send_document(chat_id=chat_id, document=types.InputFile(filepath))

@dp.message_handler(content_types=ContentType.PHOTO)
async def save_image(message: types.Message):
    chat_id = message.chat.id
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path
    filepath = Path('downloads', str(chat_id), filename)
    file = await bot.download_file(filename, filepath)
    await bot.send_document(chat_id=chat_id, document=types.InputFile(filepath))

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)