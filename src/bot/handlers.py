from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, \
                                                JOIN_TRANSITION, \
                                                LEAVE_TRANSITION

from src.collector.dao import Message
from .dao import ActiveChat


handlers_router = Router()


class RateTheBot(StatesGroup):
    confirm = State()
    rate = State()


@handlers_router.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm SpanBot!\n"
                        "I can save your messages in db.\n"
                        "You may check connection to db with command /check"
                        " or /rate this bot.")


@handlers_router.message(Command(commands=["check"]))
async def check_api_connection(message: types.Message):
    try:
        amount_messages = await Message.filter(chat_id=message.chat.id).count()
    except Exception as e:
        await message.answer("Connection to DB: Error")
        print(e)
    else:
        await message.answer("Connection to DB: OK\n"
                             f"There are {amount_messages} messages from this "
                             "chat saved in DB.")


@handlers_router.message(Command(commands="rate"))
async def want_to_rate(message: types.Message, state: FSMContext):
    await state.set_state(RateTheBot.confirm)
    await message.reply("Do you want to rate this bot?\n"
                        "(You may end the dialogue with "
                        "command /cancel at any moment)")


@handlers_router.message(Command(commands="cancel"))
async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None
    await state.clear()
    await message.reply("You quit this dialogue.")


@handlers_router.message(RateTheBot.confirm)
async def rate_bot(message: types.Message, state: FSMContext):
    if message.text.strip().lower() == "yes":
        await state.set_state(RateTheBot.rate)
        await message.reply("How do you like this bot?\n"
                            "Send your mark from 1 to 5.")
    elif message.text.strip().lower() == "no":
        await state.clear()
        await message.reply("OK! You may do it later if you want.")
    else:
        await message.reply("Sorry, I don't understand.\n"
                            "Please send 'yes' or 'no'.")


@handlers_router.message(RateTheBot.rate)
async def get_bot_rating(message: types.Message, state: FSMContext):
    mark = message.text.strip()
    if mark in ["4", "5"]:
        await message.reply(f"Your mark is {mark}.\nThanks! Nice to know it.")
        await state.clear()
    elif mark in ["1", "2", "3"]:
        await message.reply(f"Your mark is {mark}.\n"
                            "I will try to become better!")
        await state.clear()
    else:
        await message.reply("Sorry, I don't understand.\n"
                            "Please send your mark from 1 to 5.")


@handlers_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION)
)
async def bot_was_added_in_chat(event: ChatMemberUpdated):
    await ActiveChat.get_or_create(chat_id=event.chat.id)


@handlers_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION)
)
async def bot_was_kicked_from_chat(event: ChatMemberUpdated):
    await ActiveChat.filter(chat_id=event.chat.id).delete()
