import states
import re
import json
import time

from loader import dp
from data import config

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from utils.db_api import db_api, tables
from utils.models import ages, models
from utils.misc.read_file import read_txt_file

from utils.misc import regexps
from utils.classes import kb_constructor, timer, transaction

import keyboards


@dp.message_handler(state="*", commands="units")
async def units_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)
    units: tables.Units = session.filter_by_user_id(
        user_id=user_id, table=tables.Units)

    base_units = ages.Age.get_all_units()
    timer.UnitsTimer().get_creation_queue_timer(user_id=user_id)
    text = "\n"
    for queue in units.creation_queue:
        unit = base_units[units.units_type[queue["unit_num"]]]
        unit_emoji = re.findall(r"(\W+)\s+", unit.name)[0]
        time_left = timer.Timer.get_left_time(queue["timer"])

        text += "▸ <code>x{}</code> {} - [ {} {} ]\n".format(
            queue["creation_count"], unit_emoji, *time_left
        )

    keyboard = kb_constructor.StandardKeyboard(
        user_id=user_id).create_units_keyboard()

    msg_text = read_txt_file("text/units/units")
    unit_msg = await message.answer(
        text=msg_text.format(sum(units.units_count), text),
        reply_markup=keyboard
    )

    await state.set_data({
        "user_id": user_id,
        "unit_msg": unit_msg,
    })

    # await states.Units.menu.set()
    session.close()


@dp.callback_query_handler(regexp=regexps.Units.back)
async def back_units_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    unit_msg: types.Message = data.get("unit_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    if callback.data == "back_units":
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_units_keyboard()
        await unit_msg.edit_text(
            text=unit_msg.html_text,
            reply_markup=keyboard,
        )
    await callback.answer()


@dp.callback_query_handler(regexp=r"unit_(\d+)")
async def reply_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    unit_msg: types.Message = data.get("unit_msg")
    session = db_api.CreateSession()

    unit_num = re.findall(r"unit_(\d+)", callback.data)
    base_units = ages.Age.get_all_units()
    if unit_num:
        unit = base_units[int(unit_num[0])]
        msg_text = read_txt_file("text/units/about_unit")

        keyboard = keyboards.units.kb_back_units
        await unit_msg.edit_text(
            text=msg_text.format(
                unit.name,
                unit.type_unit,
                unit.damage,
                unit.armor,
                transaction.Purchase.get_price(unit.create_price),
                *timer.Timer.get_left_time_min(unit.create_time_sec)
            ),
            reply_markup=keyboard
        )

    session.close()
    await callback.answer()


@dp.message_handler(IsReplyFilter(True), regexp=r"(сделать|создать)\s+(\d+)\s+(\d+)")
async def reply_menu_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    unit_msg: types.Message = data.get("unit_msg")

    session = db_api.CreateSession()

    # table data
    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)
    units: tables.Units = session.filter_by_user_id(
        user_id=user_id, table=tables.Units)

    # age model
    base_units = ages.Age.get_all_units()
    if message.reply_to_message.message_id != unit_msg.message_id:
        return

    make_unit = re.findall(r"(\d+)\s+(\d+)", message.text)
    if make_unit:
        unit_num = int(make_unit[0][1])-1
        creating_count = int(make_unit[0][0])

        if creating_count <= 0 or unit_num < 0:
            return

        if units.units_type[unit_num] is None:
            return

        unit = base_units[units.units_type[unit_num]]
        unit_emoji = re.findall(r"(\W+)\s+", unit.name)[0]

        creating_price = list(map(
            lambda price: price*creating_count, unit.create_price
        ))

        buying = transaction.Purchase.buy(creating_price, townhall)
        if buying:
            creation_queue = list(units.creation_queue)

            new_queue = {
                "unit_num": unit_num,
                "creation_count": creating_count,
                "timer": timer.Timer.set_timer(unit.create_time_sec*creating_count)
            }
            units_num = []
            for queue in creation_queue:
                queue_index = creation_queue.index(queue)
                if queue["unit_num"] == unit_num:
                    creation_queue.remove(queue)
                    time_left = timer.Timer.get_left_time_sec(queue["timer"])
                    new_queue["creation_count"] += creating_count
                    new_queue["timer"] += time_left
                    creation_queue.insert(queue_index, new_queue)
                    units.creation_queue = creation_queue

                units_num.append(queue["unit_num"])

            if unit_num not in units_num:
                creation_queue.append(new_queue)
                units.creation_queue = creation_queue

            session.db.commit()
            text = "\n"
            for queue in units.creation_queue:
                unit = base_units[units.units_type[queue["unit_num"]]]
                unit_emoji = re.findall(r"(\W+)\s+", unit.name)[0]
                time_left = timer.Timer.get_left_time(queue["timer"])

                text += "▸  <code>x{}</code> {} - [ {} {} ]\n".format(
                    queue["creation_count"], unit_emoji, *time_left
                )

            keyboard = kb_constructor.StandardKeyboard(
                user_id=user_id).create_units_keyboard()
            msg_text = read_txt_file("text/units/units")
            await unit_msg.edit_text(
                text=msg_text.format(sum(units.units_count), text),
                reply_markup=keyboard
            )
        else:
            max_num = transaction.Purchase.get_max_create_num(unit.create_price, townhall)
            await unit_msg.reply(
                text="Тебе хватит только на x{} {}".format(
                    max_num, unit_emoji
                ))

    session.close()
