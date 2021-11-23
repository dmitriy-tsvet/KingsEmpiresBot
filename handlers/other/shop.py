import states
from loader import dp
from data import config

from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.misc.read_file import read_txt_file

from utils.db_api import db_api, tables

from utils.classes import transaction, kb_constructor, timer, table_setter, hour_income
from utils.models import ages

from utils.models import models, base
from utils.misc.regexps import TownhallRegexp

import re
import typing
import keyboards


@dp.message_handler(state="*", commands="shop")
async def shop_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_mention = message.from_user.get_mention()

    await message.answer(
        text="Магазин",
        reply_markup=keyboards.shop.kb_shop
    )


