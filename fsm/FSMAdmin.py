from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import bot_db
from keyboards.ckient_kb import cancel_markup

from config import bot, ADMIN


class FSMAdmin(StatesGroup):
    dish_photo = State()
    d_name = State()
    description = State()
    price = State()


async def fsm_dishes_start(message: types.Message):
    if message.chat.type == "private" and message.from_user.id in ADMIN:
        await FSMAdmin.dish_photo.set()
        await message.answer(f"Салам {message.from_user.full_name} пришлите фотографию блюда",
                             reply_markup=cancel_markup)
    else:
        await message.reply("Пиши в личку и только для админов !!!")


async def load_dish_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["dish_photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Название блюда")


async def load_dish_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["d_name"] = message.text
    await FSMAdmin.next()
    await message.answer("Краткое описание блюда")


async def load_dish_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMAdmin.next()
    await message.answer("Цена в сомах")


async def load_dish_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["price"] = int(message.text)
        await bot.send_photo(message.from_user.id, data["dish_photo"],
                             caption=f"Название: {data['d_name']}\n"
                                     f"Описание: {data['description']}\n"
                                     f"Цена: {data['price']}\n")
        await bot_db.sql_command_insert(state)
        await state.finish()
    except:
        await message.answer("Только число")


async def delete_dish(message: types.Message):
    if message.from_user.id in ADMIN:
        result = await bot_db.sql_command_all()
        for data in result:
            await bot.send_photo(message.from_user.id, data[0],
                                 caption=f"Название: {data[1]}\n"
                                         f"Описание: {data[2]}\n"
                                         f"Цена: {data[3]}\n",
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     f"Delete {data[1]}",
                                     callback_data=f"deldish {data[1]}"
                                 )))
    else:
        await message.answer("Вы не админ!!!")


async def complete_dishdel(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace("deldish ", ""))
    await call.answer(text=f"Dish deleted", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


async def cancel_dish_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await message.answer("Регистрация блюда отменена")
        await state.finish()


def register_handler_fsm_dishes(dp: Dispatcher):
    dp.register_message_handler(cancel_dish_registration, state="*", commands=["cancel"])
    dp.register_message_handler(cancel_dish_registration,
                                Text(equals="cancel", ignore_case=True),
                                state="*")
    dp.register_message_handler(fsm_dishes_start, commands=["dish"])
    dp.register_message_handler(load_dish_photo, state=FSMAdmin.dish_photo, content_types=["photo"])
    dp.register_message_handler(load_dish_name, state=FSMAdmin.d_name)
    dp.register_message_handler(load_dish_desc, state=FSMAdmin.description)
    dp.register_message_handler(load_dish_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_dish, commands=["delete_dish"])
    dp.register_callback_query_handler(complete_dishdel, lambda call: call.data and
                                       call.data.startswith("deldish "))
