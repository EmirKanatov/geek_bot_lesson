from aiogram import types
import random
from aiogram.utils import executor

import handlers.admin
from handlers import fsm_anketa, client, callback, extra, admin

from config import bot, dp
import logging

client.register_handler_client(dp)
callback.register_handlers_callback(dp)
admin.register_handler_admin(dp)
fsm_anketa.register_handler_fsm_anketa(dp)

extra.register_handlers_extra(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
