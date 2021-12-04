from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api import db_api, tables


@dp.message_handler(commands="start")
async def start_command_handler(message: types.Message):
    user_id = message.from_user.id

    session = db_api.CreateSession()

    user = session.db.query(tables.User).filter_by(
        user_id=user_id).first()

    if user is not None:
        await message.answer(
            text="У тебя уже есть аккаунт."
        )

    session.close()
