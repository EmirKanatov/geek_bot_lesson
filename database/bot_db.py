import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("Database is working")
    db.execute("CREATE TABLE IF NOT EXISTS menu "
               "(photo TEXT, name TEXT PRIMARY KEY,"
               "description TEXT,"
               "price INT)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO menu VALUES "
                       "(?, ?, ?, ?)", tuple(data.values()))
    db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM menu").fetchall()
    random_dish = random.choice(result)
    await bot.send_photo(message.from_user.id, random_dish["dish_photo"],
                         caption=f"Название: {random_dish['d_name']}\n"
                                 f"Описание: {random_dish['description']}\n"
                                 f"Цена: {random_dish['price']}\n")


async def sql_command_all():
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(text):
    cursor.execute("DELETE FROM menu WHERE name == ?", (text, ))
    db.commit()
