import asyncio

import random

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api import tables, db_api
from states import reg
from utils.misc.read_file import read_txt_file
from utils.classes import timer


class FinanceRegulator(BaseMiddleware):

    async def on_post_process_message(self, message: types.Message, data_from_filter: list, dat: dict):
        if message.is_command():
            user_id = message.from_user.id
            new_session = db_api.NewSession()

            townhall_table: tables.TownHall = new_session.filter_by_user_id(
                user_id=user_id, table=tables.TownHall
            )
            citizens_table: tables.Citizens = new_session.filter_by_user_id(
                user_id=user_id, table=tables.Citizens
            )
            finance_table: tables.Finance = new_session.filter_by_user_id(
                user_id=user_id, table=tables.Finance
            )
            units_table: tables.Units = new_session.filter_by_user_id(
                user_id=user_id, table=tables.Units
            )

            finance_timer = timer.FinanceTimer()
            finance_timer.get_culture_timer(
                finance_table=finance_table, citizen_table=citizens_table
            )
            finance_timer.get_economics_timer(
                finance_table=finance_table, citizen_table=citizens_table,
                townhall_table=townhall_table
            )
            finance_timer.get_army_timer(
                finance_table=finance_table, citizen_table=citizens_table,
                units_table=units_table
            )

            time_set = timer.Timer.set_timer(3600)
            finance_table.money_timer = time_set

            new_session.close()
