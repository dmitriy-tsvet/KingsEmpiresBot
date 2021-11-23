# import asyncio
#
# from aiogram import types, Dispatcher
# from aiogram.dispatcher.handler import CancelHandler, current_handler
# from aiogram.dispatcher.middlewares import BaseMiddleware
# from utils.db_api import tables, db_api
# from states import reg
# from utils.misc.read_file import read_txt_file
#
#
# class UniqueHandler(BaseMiddleware):
#     async def on_pre_process_message(self, message: types.Message, data: dict):
#         command = message.get_command()
#         list_commands = [
#             "/start", "/townhall", "/buildings", "/territory",
#             "/units", "/help", "/citizens"
#         ]
#
#         if message.is_command():
#             data.update({"user_id": message.from_user.id})
#
#     async def on_process_message(self, callback: types.CallbackQuery, data: dict):
#         if data.get("user_id") != callback.from_user.id:
#             return await callback.answer("Не твое, черт!")
#
