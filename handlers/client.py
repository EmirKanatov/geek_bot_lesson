import random

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from config import dp, bot
from database.bot_db import sql_command_random
from keyboards.ckient_kb import start_markup
from pars import movies


@dp.message_handler(commands=["meme"])
async def sendphoto(msg):
    arr = ["media/meme1.jpeg", "media/meme2.jpeg",
           "media/meme3.jpeg", "media/meme4.jpeg", "media/meme5.jpeg", "media/meme6.jpeg"]
    photo = open(random.choice(arr), "rb")
    await bot.send_photo(msg.from_user.id, photo)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Hello {message.from_user.full_name}", reply_markup=start_markup)


@dp.message_handler(commands=["dice"])
async def start_command(message: types.Message):
    bot_value = (await bot.send_dice(message.chat.id))
    user_value = (await bot.send_dice(message.chat.id))
    if bot_value.dice.value > user_value.dice.value:
        await bot.send_message(message.chat.id,
                               f"Поздравляем вы выйграли!!! у вас {user_value.dice.value} "
                               f"у бота {bot_value.dice.value}")
    elif bot_value.dice.value < user_value.dice.value:
        await bot.send_message(message.chat.id,
                               f"К сожалению вы проиграли((( у вас {user_value.dice.value}"
                               f"у бота {bot_value.dice.value}")
    else:
        await bot.send_message(message.chat.id,
                               f"Ничья ахa у обоих по {bot_value.dice.value}")


@dp.message_handler(commands=["quiz"])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("First", callback_data="question_1")
    button_2 = InlineKeyboardButton("Second", callback_data="question_2")
    button_3 = InlineKeyboardButton("Third", callback_data="question_3")
    markup.add(button_1, button_2, button_3)

    await bot.send_message(message.chat.id, "Choose question", reply_markup=markup)
    # question = "Choose question ???"
    # answer = [
    #     "1", "2", "3"
    # ]
    # await bot.send_poll(
    #     chat_id=message.chat.id,
    #     question=question,
    #     options=answer,
    #     is_anonymous=False,
    #     type='quiz',
    #     correct_option_id=0 or 1,
    #     explanation="Год барррана",
    #     explanation_parse_mode=ParseMode.MARKDOWN,
    #     reply_markup=markup,
    # )


async def show_random_user(message: types.Message):
    await sql_command_random(message)


async def parser_movies(message: types.Message):
    data = movies.parse()
    for movie in data:
        desc = movie["desc"].split(',')
        await bot.send_message(message.from_user.id, f"{movie['title']}\n"
            f"Год: {desc[0]}\n"
            f"Город: {desc[1]}\n"
            f"Жанр: {desc[2]}\n"
            f"{movie['link']}"
        )


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["skip"])
    dp.register_message_handler(sendphoto, commands=["meme"])
    dp.register_message_handler(quiz_1, commands=["quiz"])
    dp.register_message_handler(show_random_user, commands=["random"])
    dp.register_message_handler(parser_movies, commands=["film"])
