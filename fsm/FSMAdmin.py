from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
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
        await state.finish()
        await bot.send_photo(message.from_user.id, data["dish_photo"],
                             caption=f"Название: {data['d_name']}\n"
                                     f"Описание: {data['description']}\n"
                                     f"Цена: {data['price']}\n")
    except:
        await message.answer("Введите только число")



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
