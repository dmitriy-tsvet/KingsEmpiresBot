from loader import dp
from aiogram import types


@dp.callback_query_handler(state="*")
async def user_alert_handler(callback: types.CallbackQuery):
    await callback.answer("эти кнопочки не хотят работать :B")
