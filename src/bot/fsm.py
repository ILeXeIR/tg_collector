from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup



class RateTheBot(StatesGroup):
    confirm = State()
    rate = State()

#@dp.message_handler(commands=["rate"], state=None)
async def want_to_rate(message: types.Message):
    await RateTheBot.confirm.set()
    await message.reply("Do you want to rate this bot?\n"
                        + "(You may end the dialogue with command /cancel at any moment)")

#@dp.message_handler(commands=["cancel"], state="*")
async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("You quitted this dialogue.")

#@dp.message_handler(state=RateTheBot.confirm)
async def rate_bot(message: types.Message, state: FSMContext):
    if message.text.strip().lower() == "yes":
        await RateTheBot.next()
        await message.reply("How do you like this bot?\nSend your mark from 1 to 5.")
    elif message.text.strip().lower() == "no":
        await state.finish()
        await message.reply("OK! You may do it later if you want.")
    else:
        await message.reply("Sorry, I don't understand. Please send 'yes' or 'no'.")

#@dp.message_handler(state=RateTheBot.rate)
async def get_bot_rating(message: types.Message, state: FSMContext):
    mark = message.text.strip()
    if mark in ["4", "5"]:
        await message.reply(f"Your mark is {mark}. Thanks! Nice to know it.")
        await state.finish()
    elif mark in ["1", "2", "3"]:
        await message.reply(f"Your mark is {mark}. I will try to become better!")
        await state.finish()
    else:
        await message.reply("Sorry, I don't understand. Please send your mark from 1 to 5.")

def register_handler_fsm(dp: Dispatcher):
    dp.register_message_handler(want_to_rate, commands=["rate"], state=None)
    dp.register_message_handler(cancel_state, commands=["cancel"], state="*")
    dp.register_message_handler(rate_bot, state=RateTheBot.confirm)
    dp.register_message_handler(get_bot_rating, state=RateTheBot.rate)