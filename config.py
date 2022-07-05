from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

storage = MemoryStorage()

TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN = [787377130, ]
URL = "https://python-18-kanatov.herokuapp.com/"