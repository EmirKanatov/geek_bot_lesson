<<<<<<< HEAD
from aiogram import types
import random
from aiogram.utils import executor
from handlers import client, callback, extra
=======

from aiogram import types
import random
from aiogram.utils import executor
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
>>>>>>> 1b7eebe38a45532464e187293100834b79327ce7

from config import bot, dp
import logging

<<<<<<< HEAD
client.register_handler_client(dp)
callback.register_handlers_callback(dp)
extra.register_handlers_extra(dp)
=======

@dp.message_handler(commands=["skip"])
async def start_command(message: types.Message):
    await message.reply(f"Hello {message.from_user.full_name}, kak ")


@dp.message_handler(commands=["quiz"])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="button_1")
    markup.add(button_1)

    question = "Kogda rodilsya Linus Torvalds?"
    answer = [
        "1212", "2003", "1969", "1976", "1998"
    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Год барррана",
        explanation_parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda call: call.data == "button_1")
async def quiz_2(call: types.CallbackQuery):
    question = "15 в квадрате будет ... ?"
    answer = [
        "30", "125", "987", "255", "225", "252"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        explanation="Ляяя программа 7го класса",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
    )


@dp.message_handler(commands=["meme"])
async def sendphoto(msg):
    arr = ["media/meme1.jpeg", "media/meme2.jpeg",
           "media/meme3.jpeg", "media/meme4.jpeg", "media/meme5.jpeg", "media/meme6.jpeg"]
    photo = open(random.choice(arr), "rb")
    await bot.send_photo(msg.from_user.id, photo)


@dp.message_handler()
async def echo(message: types.Message):
    if(message.text.isdigit()):
        await bot.send_message(message.from_user.id,
                               int(message.text) * int(message.text))
    else:
        await bot.send_message(message.from_user.id, message.text)

>>>>>>> 1b7eebe38a45532464e187293100834b79327ce7

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
