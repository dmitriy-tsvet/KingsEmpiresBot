import asyncio

from aiogram import types, Dispatcher
from filters.reply_message import IsReplyMessage
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api import tables, db_api
from aiogram.dispatcher import FSMContext
from states import reg
from utils.misc.read_file import read_txt_file


class CheckUserRegistration(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        command = message.get_command()
        list_commands = [
            "/start", "/townhall", "/buildings", "/territory",
            "/units", "/help", "/citizens"
        ]

        if message.is_command():

            user_id = message.from_user.id
            session = db_api.Session(user_id=user_id)
            session.open_session()
            result: tables.User = session.quick_session(tables.User)

            if result is None:
                msg_text = read_txt_file("text/reg")

                await message.reply(
                    text=msg_text
                )

                session.close_session()
                await reg.Reg.input_name_country.set()
                raise CancelHandler()
            session.close_session()

    async def on_process_message(self, message: types.Message, data: dict):
        if data.get("raw_state") == "Reg:input_name_country":
            msg_text = read_txt_file("text/reg")

            if data.get("reply").text == msg_text:
                data["middleware_data"] = data.get("reply").message_id
            else:
                raise CancelHandler()


