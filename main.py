import asyncio

from aiogram.utils import executor

from handlers import notification, fsm_anketa, client, callback, extra, admin
from fsm import FSMAdmin

from config import dp, bot, URL
import logging
from database.bot_db import sql_create


async def on_startup(_):
    await bot.set_webhook(url=URL)
    asyncio.create_task(notification.scheduler())
    sql_create()


async def on_shutdown(dp):
    await bot.delete_webhook()


client.register_handler_client(dp)
callback.register_handlers_callback(dp)
admin.register_handler_admin(dp)
FSMAdmin.register_handler_fsm_dishes(dp)
fsm_anketa.register_handler_fsm_anketa(dp)
notification.register_handler_notification(dp)


extra.register_handlers_extra(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path="",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=5000
    )