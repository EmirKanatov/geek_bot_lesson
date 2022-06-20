from aiogram import Bot, Dispatcher
from decouple import config


TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
<<<<<<< HEAD
ADMIN = [787377130, ]
=======
>>>>>>> 1b7eebe38a45532464e187293100834b79327ce7
