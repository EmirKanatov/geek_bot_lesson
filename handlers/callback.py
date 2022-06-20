from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

from config import bot

# @dp.callback_query_handler(lambda call: call.data == "button_1")

polls = {
    '1': {
        "question": "15 в квадрате будет ... ?",
        "answer": ["30", "125", "987", "255", "225", "252"],
        "correct_answer": "4"
    },
    '2': {
        "question": "Компилятора это?",
        "answer": ["хз", "автомат?", "Комп такой наверное", "25", "C++"],
        "correct_answer": "4"
    },
    '3': {
        "question": "Kogda rodilsya Linus Torvalds?",
        "answer": ["1212", "2003", "1969", "1976", "1998"],
        "correct_answer": "2"
    }
}


async def quiz_2(call: types.CallbackQuery):
    result = int(call.data.split("_")[1])
    print(result)
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("First question", callback_data="question_1")
    button_2 = InlineKeyboardButton("Second question", callback_data="question_2")
    button_3 = InlineKeyboardButton("Third question", callback_data="question_3")
    markup.add(button_1, button_2, button_3)
    if len(polls) == 0:
        await bot.send_message(call.message.chat.id, "Вы ответили на все вопросы!!!")
        return
    if str(result) in polls.keys():
        await bot.send_poll(
            chat_id=call.message.chat.id,
            question=polls[f"{result}"]["question"],
            options=polls[f"{result}"]["answer"],
            is_anonymous=False,
            type='quiz',
            correct_option_id=polls[f"{result}"]["correct_answer"],
            explanation_parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=markup
        )
        polls.pop(f"{result}")
    else:
        await bot.send_message(call.message.chat.id, "Вопрос уже отрпавлен выберите другой!!!")

# async def quiz_3(call: types.CallbackQuery):
#     markup = InlineKeyboardMarkup()
#     button_2 = InlineKeyboardButton("NEXT", callback_data="button_1")
#     markup.add(button_2)
#
#     question = "Компилятора это?"
#     answer = [
#         "хз", "автомат?", "Комп такой наверное", "25", "C++"
#     ]
#     await bot.send_poll(
#         chat_id=call.message.chat.id,
#         question=question,
#         options=answer,
#         is_anonymous=False,
#         type='quiz',
#         correct_option_id=4,
#         explanation="Ля программа 7го класса",
#         explanation_parse_mode=ParseMode.MARKDOWN_V2,
#         reply_markup=markup,
#     )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, Text(startswith="question_"))
# dp.register_callback_query_handler(quiz_3, lambda call: call.data == "button_2")
