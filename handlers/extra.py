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


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
