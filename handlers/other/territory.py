import typing

import keyboards
import states
import re

from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import  IsReplyFilter

from aiogram.dispatcher import FSMContext
from utils.misc.read_file import read_txt_file
from utils.db_api import tables, db_api
from utils.ages import ages_list, models
from utils.classes import kb_constructor, timer
from utils.war_system import fight
from utils.misc.operation_with_lists import subtract_nums_list

from data import config


@dp.message_handler(chat_id=config.ADMIN, state="*", commands="territory")
@dp.throttled(rate=1)
async def territory_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    age = townhall_table.age

    territory_table: tables.Territory = session.built_in_query(tables.Territory)

    # age model
    age_model: models.Age = ages_list.AgesList.get_age_model(age)
    models_territories: typing.List[models.Territory] = age_model.territories

    owned_territory = list(territory_table.owned_territory)
    indexes_owned_territory = [i for i, x in enumerate(owned_territory) if x is True]

    capture_time_left = timer.TerritoryTimer.get_capture_timer(
        territory_table=territory_table
    )

    text = ""
    for territory in models_territories:
        index = models_territories.index(territory)

        if index == territory_table.capturing_index:
            text += "{} | <b>⚔ захват ({} {})</b>".format(
                territory.name, *capture_time_left)
        elif index in indexes_owned_territory:
            text += "{} | <b>захвачено</b>".format(territory.name)
        else:
            text += "{} |<b> x{} 🦹🏻, {}/ч. 💰</b>".format(
                territory.name, territory.unit_counts,
                territory.tax
            )

        if index != len(models_territories)-1:
            text += "\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n"

    msg_text = read_txt_file("text/territory/territory")
    edit_msg = await message.answer(
        text=msg_text.format(
            text,
            len(indexes_owned_territory)
        ),
        reply_markup=keyboards.territory.kb_territory
    )

    await state.set_data({
        "models_territories": models_territories,
        "edit_msg": edit_msg,
    })

    await states.Territory.menu.set()
    session.close_session()


@dp.callback_query_handler(state=states.Territory.menu)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    if callback.data == "back_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup,
        )
        await states.Territory.menu.set()
        return

    models_territories = data.get("models_territories")

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)

    territory_table: tables.Territory = session.built_in_query(tables.Territory)
    owned_territory = list(territory_table.owned_territory)
    indexes_owned_territory = [i for i, x in enumerate(owned_territory) if x is True]

    if callback.data == "capture":
        if territory_table.capturing_index is not None:
            capture_time_left = timer.Timer.get_left_time(territory_table.capture_timer)

            msg_text = read_txt_file("text/territory/capture_info")
            await edit_msg.edit_text(
                msg_text.format(*capture_time_left),
                reply_markup=keyboards.territory.kb_capturing
            )
            session.close_session()
            return await callback.answer("")

        keyboard = kb_constructor.StandardKeyboard(user_id=user_id)
        keyboard = keyboard.create_territory_keyboard()

        msg_text = read_txt_file("text/territory/select_territory")
        await edit_msg.edit_text(
            msg_text,
            reply_markup=keyboard
        )
        await states.Territory.select_territory.set()
    elif callback.data == "get_tax":
        if territory_table.capturing_index is not None:
            session.close_session()
            return await callback.answer("Во время захвата, нельзя собрать налог.")

        income = timer.TerritoryTimer.get_money_timer(
            territory_table,
            indexes_owned_territory,
            models_territories
        )
        townhall_table.money += income
        await callback.answer("+ {} 💰".format(income), show_alert=False)

    session.close_session()


@dp.callback_query_handler(state=states.Territory.select_territory)
async def select_territory_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    if callback.data == "back_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup,
        )
        await states.Territory.menu.set()
        return

    selected_territory = re.findall(r"territory_(\d+)", callback.data)

    if selected_territory:
        territory_index = int(selected_territory[0])
        models_territories: typing.List[models.Territory] = data.get("models_territories")

        keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
        keyboard = keyboard.create_territory_keyboard()

        msg_text = read_txt_file("text/territory/select_units")
        select_units_msg = await edit_msg.edit_text(
            text=msg_text.format(0),
            reply_markup=keyboard
        )

        await state.update_data({
            "territory_index": territory_index,
            "territory": models_territories[territory_index],
            "selected_units": 0,
            "select_units_msg": select_units_msg
        })
        await states.Territory.select_units.set()


@dp.callback_query_handler(state=states.Territory.select_units)
async def select_units_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    if callback.data == "back_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup,
        )
        await states.Territory.menu.set()
        return

    select_units_msg: types.Message = data.get("select_units_msg")
    selected_units = data.get("selected_units")
    territory: models.Territory = data.get("territory")

    keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    units_table: tables.Units = session.built_in_query(tables.Units)

    page_move = re.findall(r"page_(\d+)", callback.data)
    select_units = re.findall(r"select_units_(\d+)", callback.data)

    if page_move:
        page = int(page_move[0])
        keyboard = keyboard.create_territory_keyboard(page)
        select_units_msg = await select_units_msg.edit_reply_markup(keyboard)

        await state.update_data({
            "select_units_msg": select_units_msg
        })

    elif select_units:
        selected_units += int(select_units[0])

        if selected_units > units_table.all_unit_counts:
            session.close_session()
            return await callback.answer("У вас нету столько воинов.")

        msg_text = read_txt_file("text/territory/select_units")
        await edit_msg.edit_text(
            text=msg_text.format(selected_units),
            reply_markup=select_units_msg.reply_markup
        )
        await state.update_data({
            "selected_units": selected_units
        })

    elif callback.data == "waiting_capture":

        if selected_units == 0:
            session.close_session()
            return await callback.answer(
                "Вы не выбрали кол-во воинов для захвата."
            )

        msg_text = read_txt_file("text/territory/territory_info")
        await edit_msg.edit_text(
            text=msg_text.format(
                territory.name,
                territory.tax,
                territory.unit_counts,
                selected_units
            ),
            reply_markup=keyboards.territory.kb_waiting_capture
        )

        await states.Territory.waiting_capture.set()

    await callback.answer()
    session.close_session()


@dp.message_handler(IsReplyFilter(True), state=states.Territory.select_units)
@dp.throttled(rate=2)
async def reply_menu_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    edit_msg: types.Message = data.get("edit_msg")
    selected_units = data.get("selected_units")
    select_units_msg: types.Message = data.get("select_units_msg")

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    units_table: tables.Units = session.built_in_query(tables.Units)

    if message.reply_to_message.message_id == edit_msg.message_id:
        count_selected_units = re.findall(r"(\d+)", message.text)
        if not count_selected_units:
            session.close_session()
            return

        selected_units += int(count_selected_units[0])

        if selected_units > units_table.all_unit_counts:
            session.close_session()
            return await message.reply("У вас нету столько воинов.")

        msg_text = read_txt_file("text/territory/select_units")
        await edit_msg.edit_text(
            text=msg_text.format(selected_units),
            reply_markup=select_units_msg.reply_markup
        )
        await state.update_data({
            "selected_units": selected_units
        })

    session.close_session()


@dp.callback_query_handler(state=states.Territory.waiting_capture)
async def waiting_capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    if callback.data == "back_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup,
        )
        await states.Territory.menu.set()
        return

    selected_units: int = data.get("selected_units")
    territory: models.Territory = data.get("territory")
    territory_index: int = data.get("territory_index")

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    territory_table: tables.Territory = session.built_in_query(tables.Territory)
    units_table: tables.Units = session.built_in_query(tables.Units)
    unit_counts = list(units_table.unit_counts)

    if callback.data == "start_capture":
        time_set: int = timer.Timer().set_timer(territory.time_capture_sec)
        unit_counts: list = subtract_nums_list(selected_units, unit_counts)
        
        territory_table.capturing_index = territory_index
        territory_table.capture_timer = time_set
        units_table.all_unit_counts -= selected_units
        units_table.unit_counts = unit_counts

        win_fight: str = fight(selected_units, territory.unit_counts)

        if win_fight == "attacker":
            territory_table.capture_state = "win"
        else:
            territory_table.capture_state = "lose"

        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup
        )
        await states.Territory.menu.set()

    await callback.answer()
    session.close_session()

