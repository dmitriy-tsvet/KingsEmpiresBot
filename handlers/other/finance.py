from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from utils.misc.read_file import read_txt_file

from utils.classes import kb_constructor, timer
from utils.db_api import db_api, tables
from utils.ages import models
from utils.classes import finance_regulator

import states
import re
import keyboards


@dp.message_handler(state="*", commands="finance")
async def market_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id
    )
    keyboard = keyboard.create_finance_keyboard()
    #

    new_session = db_api.NewSession()
    finance_table: tables.Finance = new_session.filter_by_user_id(
        user_id=user_id, table=tables.Finance
    )

    msg_text = read_txt_file("text/finance")
    edit_msg = await message.answer(
        text=msg_text.format(
            finance_table.culture,
            finance_table.economics,
            finance_table.army
        ),
        reply_markup=keyboard
    )

    new_session.close()
    await state.set_data({
        "edit_msg": edit_msg
    })
    await states.Finance.menu.set()


@dp.callback_query_handler(state=states.Finance.menu)
async def callback_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = callback.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    new_session = db_api.NewSession()
    finance_table: tables.Finance = new_session.filter_by_user_id(
        user_id=user_id, table=tables.Finance
    )
    townhall_table: tables.TownHall = new_session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall
    )

    page_move = re.findall(r"page_(\d+)", callback.data)

    if page_move:
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id
        )
        page = int(page_move[0])
        keyboard = keyboard.create_finance_keyboard(page)
        edit_msg = await edit_msg.edit_reply_markup(reply_markup=keyboard)
        await state.update_data({
            "edit_msg": edit_msg
        })

    elif callback.data == "culture":
        finance_sum = int(edit_msg.reply_markup.inline_keyboard[1][1].callback_data)
        if townhall_table.money < finance_sum:
            new_session.close()
            msg_text = read_txt_file("text/hints/few_money")
            return await callback.answer(
                text=msg_text
            )
        townhall_table.money -= finance_sum
        finance_table.culture += finance_sum

    elif callback.data == "economics":
        finance_sum = int(edit_msg.reply_markup.inline_keyboard[1][1].callback_data)
        if townhall_table.money < finance_sum:
            new_session.close()
            msg_text = read_txt_file("text/hints/few_money")
            return await callback.answer(
                text=msg_text
            )
        townhall_table.money -= finance_sum
        finance_table.economics += finance_sum

    elif callback.data == "army":
        finance_sum = int(edit_msg.reply_markup.inline_keyboard[1][1].callback_data)
        if townhall_table.money < finance_sum:
            new_session.close()
            msg_text = read_txt_file("text/hints/few_money")
            return await callback.answer(
                text=msg_text
            )
        townhall_table.money -= finance_sum
        finance_table.army += finance_sum

    if callback.data in ("army", "economics", "culture"):
        msg_text = read_txt_file("text/finance")
        edit_msg = await edit_msg.edit_text(
            text=msg_text.format(
                finance_table.culture,
                finance_table.economics,
                finance_table.army
            ),
            reply_markup=edit_msg.reply_markup
        )
        await state.set_data({
            "edit_msg": edit_msg
        })
    await callback.answer()
    new_session.close()
