from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import ContentTypes
import keyboards


from data import config


@dp.message_handler(chat_id=config.ADMIN, content_types=ContentTypes.STICKER)
async def start_handler(message: types.Message):
    await message.answer(message.sticker.file_id)
