import random

from aiogram import types, Dispatcher
from config import bot, ADMIN


# @dp.message_handler()
async def echo(message: types.Message):
    if message.text.isdigit():
        await bot.send_message(message.chat.id,
                               int(message.text) * int(message.text))
    else:
        await bot.send_message(message.chat.id, message.text)
    if message.text.startswith("pin") and message.reply_to_message:
        await bot.pin_chat_message(message.chat.id, message.message_id)

    if message.text.startswith("game"):
        if message.from_user.id in ADMIN:
            emojyes = ["⚽", "🏀", "🎲", "🎯", "🎳", "🎰"]
            choose = random.randint(0, len(emojyes) - 1)
            await bot.send_dice(message.chat.id, emoji=emojyes[choose])
        else:
            await bot.send_message(message.chat.id, "Вы не являетесь администратором")

    if message.text.startswith("seconds"):
        seconds = int(message.text.replace("seconds ", ""))
        if seconds <= 359999:
            h = seconds // 3600
            m = seconds // 60 % 60
            s = seconds % 60
            await bot.send_message(message.chat.id, f"{h}:{m}:{s}")
        else:
            await bot.send_message(message.chat.id, "less than 359999")


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
