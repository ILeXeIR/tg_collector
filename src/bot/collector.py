from datetime import datetime

from aiogram import Router, types
import requests

from src import settings


router = Router()
API_URL = settings.TG_BOT_API_URL

def make_dict(obj):
    for key in obj:
        if len(type(obj[key]).mro()) > 3:
            obj[key] = dict(obj[key])
            make_dict(obj[key])
        elif isinstance(obj[key], list):
            for i in range(len(obj[key])):
                if len(type(obj[key][i]).mro()) > 3:
                    obj[key][i] = dict(obj[key][i])
                    make_dict(obj[key][i])
        elif isinstance(obj[key], dict):
            make_dict(obj[key])

@router.message()
async def send_message(message: types.Message):
    data = dict(message)
    data["date"] = data["date"].strftime("%d.%m.%Y %H:%M:%S")
    data["content_type"] = message.content_type
    make_dict(data)
    response = requests.post(f"{API_URL}messages", json=data)
    # await message.reply(response.status_code)


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
