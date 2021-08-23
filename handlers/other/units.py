import states
import re
import json

from loader import dp
from data import config

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from utils.db_api import db_api, tables
from utils.ages import ages_list, models
from utils.misc.read_file import read_txt_file
from utils.classes import kb_constructor, timer, transaction

import keyboards


@dp.message_handler(chat_id=config.ADMIN, state="*", commands="units")
async def units_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # session
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    age = townhall_table.age

    units_table: tables.Units = session.built_in_query(tables.Units)

    # model of age
    units_model: tuple = ages_list.AgesList.get_age_model(age).units

    # timer
    units_timer = timer.UnitsTimer()
    units_timer.get_create_timer(units_table)

    # keyboard
    keyboard = kb_constructor.StandardKeyboard(user_id=user_id)
    keyboard = keyboard.create_units_keyboard()

    msg_text = read_txt_file("text/units/units")

    text = ""
    for index in range(0, len(units_model)):
        if index > 0:
            text += "\n⋯⋯⋯⋯⋯⋯⋯⋯\n"

        creation_count = units_table.creation_queue[index]
        create_time_left = timer.Timer.get_left_time(units_table.creation_timer[index])
        emoji = re.findall(r"(\W)\s", units_model[index].name)[0]
        text += "⏰ {} {} | {} {}".format(*create_time_left, emoji, int(creation_count))

    edit_msg = await message.answer(
        text=msg_text.format(
            units_table.all_unit_counts,
            text
        ),
        reply_markup=keyboard
    )
    await state.set_data({
        "edit_msg": edit_msg,
        "units_model": units_model
    })

    await states.Units.menu.set()
    session.close_session()


@dp.callback_query_handler(state=states.Units.menu)
async def units_menu_handler(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    edit_msg = data.get("edit_msg")

    user_id = callback.from_user.id

    session = db_api.Session(user_id=user_id)
    session.open_session()

    # table data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    units_table: tables.Units = session.built_in_query(tables.Units)

    levels = units_table.levels
    age = townhall_table.age

    # age model
    units_model: tuple = ages_list.AgesList.get_age_model(age).units

    num_unit = re.findall(r"check_unit_(\d+)", callback.data)
    create_unit = re.findall(r"create_unit_(\d+)", callback.data)

    if num_unit:
        num_unit = int(num_unit[0])

        current_unit = units_model[num_unit]
        current_unit_lvl = levels[num_unit]
        current_weight = current_unit.get_current_weight(
            current_unit_lvl)
        current_create_time = current_unit.get_current_create_time(
            current_unit_lvl)
        current_create_time = timer.UnitsTimer.get_create_time_left(current_create_time)

        msg_text = read_txt_file("text/units/about_unit")
        await edit_msg.edit_text(
            text=msg_text.format(
                current_unit.name,
                current_unit_lvl,
                *current_create_time,
                current_weight,
            ),
            reply_markup=keyboards.units.kb_about_unit
        )

        await callback.answer()
        await state.update_data({
            "num_unit": num_unit,
        })
        await states.Units.about_unit.set()

    elif create_unit:
        num_unit = int(create_unit[0])

        current_unit = units_model[num_unit]
        base_price = current_unit.create_price
        create_price = list(map(lambda x: x*units_table.creation_value, base_price))

        result_transaction = transaction.Transaction.subtract_resources(
            create_price, townhall_table)

        if result_transaction:
            time_set = timer.UnitsTimer()
            time_set.set_create_timer(units_table, num_unit, current_unit, units_table.creation_value)

            text = ""
            for index in range(0, len(units_model)):
                if index > 0:
                    text += "\n⋯⋯⋯⋯⋯⋯⋯⋯\n"

                creation_count = units_table.creation_queue[index]
                create_time_left = timer.Timer.get_left_time(units_table.creation_timer[index])
                emoji = re.findall(r"(\W)\s", units_model[index].name)[0]
                text += "⏰ {} {} | {} {}".format(*create_time_left, emoji, int(creation_count))

            msg_text = read_txt_file("text/units/units")
            edit_msg = await data["edit_msg"].edit_text(
                text=msg_text.format(
                    units_table.all_unit_counts,
                    text
                ),
                reply_markup=data["edit_msg"].reply_markup

            )
            await state.update_data({"edit_msg": edit_msg})
            await callback.answer()

        else:
            result = transaction.Transaction().get_max_create_num(base_price, townhall_table)
            if result != 0:
                msg_text = read_txt_file("text/hints/max_create_num")
                await callback.answer(
                    msg_text.format(result, "💂")
                )
            else:
                msg_text = read_txt_file("text/hints/few_resources")
                await callback.answer(
                    msg_text
                )

    elif callback.data == "unit_upgrading":
        time_left = timer.Timer.get_left_time(units_table.upgrade_timer)
        await callback.answer(
            "⏱ Осталось: {} {}".format(*time_left)
        )
    elif callback.data == "unit_locked":
        await callback.answer(
            text="🔐 Станет доступно в следующих веках."
        )
    else:
        await callback.answer("")

    session.close_session()


@dp.message_handler(IsReplyFilter(True), state=states.Units.menu)
async def reply_menu_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    session = db_api.Session(user_id=user_id)
    session.open_session()

    # table data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    units_table: tables.Units = session.built_in_query(tables.Units)

    age = townhall_table.age

    # age model
    units_model: tuple = ages_list.AgesList.get_age_model(age).units

    if message.reply_to_message.message_id == edit_msg.message_id:
        make_unit = re.findall(r"(\d+)\s(\d+)", message.text)
        cancel_create = re.findall(r"[О, о]тменить", message.text)
        set_creation_value = re.findall(r"[S, s]et\s(\d+)", message.text)

        if make_unit:
            num_unit = int(make_unit[0][0])-1
            creating_count = int(make_unit[0][1])

            if num_unit >= 0 or num_unit <= len(units_model)-1:
                current_unit = units_model[num_unit]
                base_price = current_unit.create_price
                create_price = list(map(lambda x: x * creating_count, base_price))

                result_transaction = transaction.Transaction.subtract_resources(
                    create_price, townhall_table)

                if result_transaction:
                    time_set = timer.UnitsTimer()
                    time_set.set_create_timer(units_table, num_unit, current_unit, creating_count)

                    text = ""
                    for index in range(0, len(units_model)):
                        if index > 0:
                            text += "\n⋯⋯⋯⋯⋯⋯⋯⋯\n"

                        creation_count = units_table.creation_queue[index]
                        create_time_left = timer.Timer.get_left_time(units_table.creation_timer[index])
                        emoji = re.findall(r"(\W)\s", units_model[index].name)[0]
                        text += "⏰ {} {} | {} {}".format(*create_time_left, emoji, int(creation_count))

                    msg_text = read_txt_file("text/units/units")
                    edit_msg = await edit_msg.edit_text(
                        text=msg_text.format(
                            units_table.all_unit_counts,
                            text
                        ),
                        reply_markup=data["edit_msg"].reply_markup

                    )
                    await state.update_data({"edit_msg": edit_msg})
                else:
                    result = transaction.Transaction().get_max_create_num(base_price, townhall_table)
                    if result != 0:
                        msg_text = read_txt_file("text/hints/max_create_num")
                        await message.reply(
                            msg_text.format(result, "💂")
                        )
                    else:
                        msg_text = read_txt_file("text/hints/few_resources")
                        await message.reply(
                            msg_text
                        )

        elif set_creation_value:
            units_table.creation_value = int(set_creation_value[0])

        elif cancel_create:
            units_empty_list = [
                0 for i in range(0, len(units_model))
            ]

            text = ""
            for index in range(0, len(units_model)):
                if index > 0:
                    text += "\n⋯⋯⋯⋯⋯⋯⋯⋯\n"

                emoji = re.findall(r"(\W)\s", units_model[index].name)[0]
                text += "⏰ {} {} | {} {}".format(0, "сек.", emoji, 0)

            msg_text = read_txt_file("text/units/units")
            await edit_msg.edit_text(
                text=msg_text.format(units_table.all_unit_counts, text),
                reply_markup=data["edit_msg"].reply_markup
            )
            
            units_table.creation_queue = units_empty_list
            units_table.creation_timer = units_empty_list

    session.close_session()


@dp.callback_query_handler(state=states.Units.about_unit)
async def units_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "back_menu_units":
        await data["edit_msg"].edit_text(
            text=data["edit_msg"].html_text,
            reply_markup=data["edit_msg"].reply_markup,
        )
        await callback.answer()
        await states.Units.menu.set()
        return

    user_id = callback.from_user.id
    num_unit = data.get("num_unit")

    # session
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # table data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    units_table: tables.Units = session.built_in_query(tables.Units)

    levels = list(units_table.levels)
    age = townhall_table.age

    # units model
    units_model: tuple = ages_list.AgesList.get_age_model(age).units
    current_unit = units_model[num_unit]

    max_lvl = current_unit.max_lvl
    upgrade_price = current_unit.upgrade_price

    if callback.data == "upgrade_unit":
        upgrade_time_left = timer.Timer.get_left_time(units_table.upgrade_timer)

        if upgrade_time_left[0] > 0:
            session.close_session()
            return await callback.answer(
                text="✨ Уже идёт прокачка."
            )

        current_level = levels[num_unit]

        if current_level > max_lvl:
            session.close_session()
            msg_text = read_txt_file("text/hints/max_lvl")
            return await callback.answer(
                text=msg_text
            )

        result_transaction = transaction.Transaction.subtract_resources(upgrade_price, townhall_table)

        if result_transaction:
            units_table.unit_num = num_unit
            units_table.levels = levels

            timer.Timer.set_upgrade_timer(units_table, current_unit)
            session.close_session()

            keyboard = kb_constructor.StandardKeyboard(
                user_id=user_id
            )
            keyboard = keyboard.create_units_keyboard()
            edit_msg = await data["edit_msg"].edit_text(
                text=data["edit_msg"].html_text,
                reply_markup=keyboard,
            )
            await state.update_data({
                "edit_msg": edit_msg
            })
            await states.Units.menu.set()
            return

        else:
            price = transaction.Transaction.get_text_price(upgrade_price)
            msg_text = read_txt_file("text/hints/price")
            await callback.answer(
                msg_text.format(price)
            )

    await callback.answer()
    session.close_session()
