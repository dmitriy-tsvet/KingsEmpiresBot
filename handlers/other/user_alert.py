from loader import dp
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import ContentTypes


@dp.callback_query_handler(state="*")
async def user_alert_handler(callback: types.CallbackQuery):
    await callback.answer("эти кнопочки не хотят работать :B")


@dp.message_handler(state="*")
@dp.throttled(rate=5)
async def user_alert_handler(message: types.Message):
    if message.is_command():
        await message.reply("🚧 тех. работы :B")
