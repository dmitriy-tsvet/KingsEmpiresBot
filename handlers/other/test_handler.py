from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import ContentTypes
import keyboards
from utils.misc.read_file import read_txt_file

from data import config

import time


@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        text="Разбан",
        url="https://www.google.com/"
    )
    keyboard.add(btn)

    await message.answer(
        text="Привет, мы надеемся, что ты осознал"
             "\nсвою вину и хочешь исправиться.\n\n"
             "За все ошибки нужно платить\n"
             "и ты не исключение.\n\n"
             "<b>Стоимость 1 разабана - 50 руб.</b>\n"
             "⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n"
             "<b>Стоимость 2 разбана - 100 руб.</b>\n"
             "⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n"
             "<b>Стоимость 3+ разбана - 200 руб.</b>\n\n"
             "<i>Все деньги с разбана идут в\n"
             "благотворительный фонд.</i>",
        reply_markup=keyboard
    )

    time.sleep(5)
    await message.answer("Вы разбанены! Больше не дури.")
    await bot.restrict_chat_member(
        chat_id=-1001632262433,
        user_id=message.from_user.id,
        permissions=types.ChatPermissions(
            can_send_messages=True
        )
    )
