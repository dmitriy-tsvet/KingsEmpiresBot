import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api import tables, db_api
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
            new_session = db_api.NewSession()
            user_table: tables.User = new_session.filter_by_user_id(
                user_id=message.from_user.id,
                table=tables.User
            )

            if user_table is None:
                msg_text = read_txt_file("text/reg")

                await message.reply(
                    text=msg_text
                )

                new_session.close()
                await reg.Reg.input_name_country.set()
                raise CancelHandler()
            new_session.close()

    async def on_process_message(self, message: types.Message, data: dict):
        if data.get("raw_state") == "Reg:input_name_country":
            msg_text = read_txt_file("text/reg")

            if data.get("reply").text == msg_text:
                data["middleware_data"] = data.get("reply").message_id
            else:
                raise CancelHandler()


