from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

quiz_button = KeyboardButton("/quiz")
location_button = KeyboardButton("/send location", request_location=True)
start_button = KeyboardButton("/start")

start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_markup.row(start_button, quiz_button, location_button)
