from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = "5445619231:AAGJzPRVngNIiV2F8hP6s4FoN3qKYNDNDSA"
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN = [787377130, ]
URL = "https://python-18-kanatov.herokuapp.com/"