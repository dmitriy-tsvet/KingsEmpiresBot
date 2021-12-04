from loader import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api import tables, db_api
from states import reg
from utils.misc.read_file import read_txt_file


class CheckUserRegistration(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):

        user_id = message.from_user.id
        bot_me = await bot.get_me()
        bot_username = bot_me.username
        list_commands = await bot.get_my_commands()
        list_commands_str = ["/{}".format(command.command) for command in list_commands]
        list_commands_with_username = [
            "/{}@{}".format(command.command, bot_username) for command in list_commands
        ]
        list_commands_str += list_commands_with_username

        list_commands_str.append("/start")
        list_commands_str.append("/start@{}".format(bot_username))

        if message.is_command():
            command = message.get_command()
            if command not in list_commands_str:
                return

            session = db_api.CreateSession()

            user_table: tables.User = session.db.query(
                tables.User).filter_by(user_id=user_id).first()

            if user_table is None:
                msg_text = read_txt_file("text/reg")

                await message.reply(
                    text=msg_text
                )

                session.close()
                await reg.Reg.input_name_country.set()
                raise CancelHandler()
            session.close()

    async def on_process_message(self, message: types.Message, data: dict):

        if data.get("raw_state") == "Reg:input_name_country":
            msg_text = read_txt_file("text/reg")

            if data.get("reply").html_text == msg_text:
                data["middleware_data"] = data.get("reply").message_id
            else:
                raise CancelHandler()


