from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.ckient_kb import cancel_markup

from config import bot


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
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Ваше имя ")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.answer("Ваша фамилия")


async def load_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["surname"] = message.text
    await FSMAdmin.next()
    await message.answer("Ваш год рождения")


async def load_age(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["age"] = 2022 - int(message.text)
        await FSMAdmin.next()
        await message.answer("Город или село в котором живете?")
    except:
        await message.answer("Введите число!!!")


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["region"] = message.text
        await bot.send_photo(message.from_user.id, data["photo"],
                             caption=f"Имя: {data['name']}\n"
                                     f"Фамилия: {data['surname']}\n"
                                     f"Возраст: {data['age']}\n"
                                     f"Регион: {data['region']}\n")
    await state.finish()


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await message.answer("Регистрация отменена")
        await state.finish()


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
