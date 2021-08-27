import re
import states
import random
import json

from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter

from utils.misc.read_file import read_txt_file
from utils.classes import table_setter, kb_constructor
from utils.ages import models, ages_list
from utils.db_api import db_api, tables

from data import config


@dp.message_handler(IsReplyFilter(True), state=states.Reg.input_name_country, chat_id=config.ADMIN)
@dp.throttled(rate=1)
async def registration_handler(message: types.Message, middleware_data, state: FSMContext):
    user_id = message.from_user.id
    user_mention = message.from_user.get_mention()

    if message.reply_to_message.message_id == middleware_data:
        result1 = re.findall(r"[a-zA-Z_]+", message.text)
        result2 = re.findall(r"[a-zA-Z_0-9]+", message.text)[:1]

        if not result1:
            return await message.reply(
                "Попробуй ещё раз.\n\n"
                "<i>Примеры: </i><code>NameCountry,\n"
                "Name_Country</code>"
            )

        else:
            country_name = result2[0]

            session = db_api.NewSession()

            new_table = table_setter.TableSetter(user_id=user_id)
            new_table.set_stone_age(message, country_name)

            townhall_table: tables.TownHall = session.filter_by_user_id(
                user_id=user_id, table=tables.TownHall)
            citizens_table: tables.Citizens = session.filter_by_user_id(
                user_id=user_id, table=tables.Citizens)

            age = townhall_table.age

            # age model
            age_model: models.Age = ages_list.AgesList.get_age_model(age)

            # keyboard
            kb_townhall = kb_constructor.StandardKeyboard(user_id=user_id)
            kb_townhall = kb_townhall.create_townhall_keyboard(age)

            with open(age_model.townhall_img, 'rb') as sticker:
                await message.answer_sticker(sticker=sticker)

            msg_text = read_txt_file("text/townhall/townhall")
            edit_msg = await message.answer(
                text=msg_text.format(
                    townhall_table.country_name,
                    citizens_table.population, citizens_table.capacity,
                    townhall_table.age, age_model.rank, user_mention
                ),
                reply_markup=kb_townhall
            )
            await state.set_data({
                "edit_msg": edit_msg,
            })
            await states.Townhall.menu.set()
            session.close()
