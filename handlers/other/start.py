from loader import dp
from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from utils.misc.read_file import read_txt_file


@dp.message_handler(chat_id=-1001316092745, state="*", commands="start", )
async def handler_private_start(message: types.Message, state: FSMContext):
    pass
