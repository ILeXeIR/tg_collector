from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class RateTheBot(StatesGroup):
    confirm = State()
    rate = State()

@router.message(Command(commands="rate"))
async def want_to_rate(message: types.Message, state: FSMContext):
    await state.set_state(RateTheBot.confirm)
    await message.reply("Do you want to rate this bot?\n"
                        + "(You may end the dialogue with command /cancel at any moment)")

@router.message(Command(commands=["cancel"]))
async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply("You quitted this dialogue.")

@router.message(RateTheBot.confirm)
async def rate_bot(message: types.Message, state: FSMContext):
    if message.text.strip().lower() == "yes":
        await state.set_state(RateTheBot.rate)
        await message.reply("How do you like this bot?\nSend your mark from 1 to 5.")
    elif message.text.strip().lower() == "no":
        await state.clear()
        await message.reply("OK! You may do it later if you want.")
    else:
        await message.reply("Sorry, I don't understand. Please send 'yes' or 'no'.")

@router.message(RateTheBot.rate)
async def get_bot_rating(message: types.Message, state: FSMContext):
    mark = message.text.strip()
    if mark in ["4", "5"]:
        await message.reply(f"Your mark is {mark}. Thanks! Nice to know it.")
        await state.clear()
    elif mark in ["1", "2", "3"]:
        await message.reply(f"Your mark is {mark}. I will try to become better!")
        await state.clear()
    else:
        await message.reply("Sorry, I don't understand. Please send your mark from 1 to 5.")
