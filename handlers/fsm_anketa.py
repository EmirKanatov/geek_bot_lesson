from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.ckient_kb import cancel_markup
from database import bot_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import bot, ADMIN


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    surname = State()
    age = State()
    region = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.photo.set()
        await message.answer(f"Салам {message.from_user.full_name} пришлите фотографию",
                             reply_markup=cancel_markup)
    else:
        await message.reply("Пиши в личку!!!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f'@{message.from_user.username}'
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Ваше имя ", reply_markup=cancel_markup)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.answer("Ваша фамилия", reply_markup=cancel_markup)


async def load_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["surname"] = message.text
    await FSMAdmin.next()
    await message.answer("Ваш год рождения", reply_markup=cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["age"] = 2022 - int(message.text)
        await FSMAdmin.next()
        await message.answer("Город или село в котором живете?", reply_markup=cancel_markup)
    except:
        await message.answer("Введите число!!!")


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["region"] = message.text
        await bot.send_photo(message.from_user.id, data["photo"],
                             caption=f"Имя: {data['name']}\n"
                                     f"Фамилия: {data['surname']}\n"
                                     f"Возраст: {data['age']}\n"
                                     f"Регион: {data['region']}\n"
                                     f"@{data['username']}")
    await bot_db.sql_command_insert(state)
    await state.finish()


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await message.answer("Регистрация отменена")
        await state.finish()


async def delete_data(message: types.Message):
    if message.from_user.id in ADMIN:
        result = await bot_db.sql_command_all()
        for user in result:
            await bot.send_photo(message.from_user.id, user[2],
                                 caption=f"Имя: {user[3]}\n"
                                         f"Фамилия: {user[4]}\n"
                                         f"Возраст: {user[5]}\n"
                                         f"Регион: {user[6]}\n"
                                         f"@{user[1]}",
                                 reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     f"Delete {user[3]}",
                                     callback_data=f"delete {user[0]}"
                                )))
    else:
        await message.answer("Вы не админ!!!")


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text=f"User deleted", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handler_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands=["cancel"])
    dp.register_message_handler(cancel_registration,
                                Text(equals="cancel", ignore_case=True),
                                state="*")
    dp.register_message_handler(fsm_start, commands=["anketa"])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_surname, state=FSMAdmin.surname)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_region, state=FSMAdmin.region)
    dp.register_message_handler(delete_data, commands=["del"])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and
                                       call.data.startswith("delete "))
