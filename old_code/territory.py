import re

from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import IsReplyFilter, Regexp

from utils.db_api.db_api2 import get_territory_table, update_table_data, get_townhall_table, update_json_column
from utils.misc.timer import get_timer_end_war, get_timer_start_war, set_timer_end_war, \
    set_timer_start_war, set_timer_free_capture, get_time_left
from keyboards.territory import *
from states.territory import Territory
from utils.misc.read_file import read_txt_file


resource_rus = {
    "food": "Провизия",
    "stock": "Сырье",
    "energy": "Энергия",
    "graviton": "Гравитон",
}

territory_db_columns = [
    "first_territory", "second_territory",
    "third_territory", "fourth_territory",
    "fifth_territory", "sixth_territory"
]

regex_capture_territory = r"capture_|back_"


async def reset_event_territory(territories, territories_names, timer_capture, territory_hash):

    for i in territories:
        if i["event"] == "free_capture" and timer_capture < 0:
            index = territories_names.index(i["territory"])
            column = territory_db_columns[index]

            i.update({
                "event": None
            })

            await update_json_column(
                user_id=territory_hash,
                column=column,
                data=i,
                table="territory"
            )
            break


@dp.message_handler(state="*", commands="territory")
async def territory_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    townhall_table = await get_townhall_table(user_id)
    territory_hash = townhall_table["territory_hash"]
    territory_timer = townhall_table["territory_timer"]
    timer_capture = await get_time_left(territory_timer)

    territory_table = await get_territory_table(territory_hash)
    timer_start_war = await get_timer_start_war(territory_table["start_timer"])
    timer_end_war = await get_timer_end_war(territory_table["end_timer"])
    war_state = territory_table["war_state"]

    first_territory = territory_table["first_territory"]
    second_territory = territory_table["second_territory"]
    third_territory = territory_table["third_territory"]
    fourth_territory = territory_table["fourth_territory"]
    fifth_territory = territory_table["fifth_territory"]
    sixth_territory = territory_table["sixth_territory"]

    territories = [
        first_territory, second_territory, third_territory,
        fourth_territory, fifth_territory, sixth_territory
        ]

    territories_names = [i["territory"] for i in territories]
    territories_resources = [i["resource"] for i in territories]
    territories_resources_emoji = []
    territories_owners_name = []
    territories_units_count = []

    for i in territories:
        if i["owner_name"] is None:
            owner = "свободно"
        else:
            owner = "👑 {}".format(i["owner_name"])

        if i["event"] == "free_capture":
            owner = "⚔ захват"

        if i["units_count"] is None:
            i["units_count"] = 0

        territories_resources_emoji.append(resource_emoji[i["resource"]])
        territories_owners_name.append(owner)
        territories_units_count.append(i["units_count"])

    if war_state == "preparation" and timer_start_war > 0:
        await message.answer(
            "<b>⚔ Территория</b>\n"
            "\n"
            "До начала новой войны\n"
            "осталось {}".format(timer_start_war)
        )

    elif war_state == "preparation" and timer_start_war <= 0:
        timer = await set_timer_end_war(territory_hash)

        await update_table_data(
            user_id=territory_hash,
            data={
                "war_state": "capture",
            },
            table="territory")

        await reset_event_territory(
            territories, territories_names,
            timer_capture, territory_hash
        )

        msg_text = read_txt_file("territory_begin")
        edit_msg = await message.answer(
            text=msg_text.format(
                *territories_resources_emoji,
                *territories_names,
                *territories_owners_name,
                timer
            ),
            reply_markup=kb_territory
        )
        await state.set_data({
            "edit_msg": edit_msg,
            "territories": territories,
            "territories_names": territories_names,
            "territories_resources": territories_resources,
            "territories_resources_emoji": territories_resources_emoji,
            "territories_owners_name": territories_owners_name,
            "territories_units_count": territories_units_count,
            "territory_timer": territory_timer,
            "territory_hash": territory_hash,
        })
        await Territory.menu_territory.set()

    elif war_state == "capture" and timer_end_war > 0:

        await reset_event_territory(
            territories, territories_names,
            timer_capture, territory_hash
        )

        msg_text = read_txt_file("territory_begin")
        edit_msg = await message.answer(
            text=msg_text.format(
                *territories_resources_emoji,
                *territories_names,
                *territories_owners_name,
                timer_end_war
            ),
            reply_markup=kb_territory
        )
        await state.set_data({
            "edit_msg": edit_msg,
            "territories": territories,
            "territories_names": territories_names,
            "territories_resources": territories_resources,
            "territories_owners_name": territories_owners_name,
            "territories_units_count": territories_units_count,
            "territory_timer": territory_timer,
            "territory_hash": territory_hash,
        })
        await Territory.menu_territory.set()

    elif war_state == "capture" and timer_end_war <= 0:
        await update_table_data(
            user_id=territory_hash,
            data={
                "war_state": "preparation",
            },
            table="territory")

        x = await set_timer_start_war(territory_hash)
        await message.answer(
            "<b>⚔ Территория</b>\n"
            "<code>◄ Война закончилась! ►</code>\n\n"
            "<code>До начала войны: </code>{}\n".format(x),
            reply_markup=kb_territory
        )


@dp.callback_query_handler(state=Territory.menu_territory)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    edit_msg = data.get("edit_msg")
    territories = data.get("territories")
    territories_names = data.get("territories_names")
    territory_hash = data.get("territory_hash")

    townhall_table = await get_townhall_table(user_id)
    country_name = townhall_table["country_name"]

    if callback.data == "capture":

        territory_timer = data.get("territory_timer")
        time_left = await get_time_left(territory_timer)

        territory_name = None
        for i in territories:
            if i["owner_name"] == country_name and i["event"] == "free_capture":
                territory_name = i["territory"]
                break

        if time_left > 0:
            await edit_msg.edit_text(
                text="<b>⚔ Территория</b>\n"
                     "<code>◄ Захват территории. ►</code>\n\n"
                     "Вы захватываете {}.\n\n"
                     "<code>Осталось: {}</code>".format(territory_name, time_left),
                reply_markup=kb_capture_in_process
            )

            await Territory.capture_in_process.set()
            return

        btn_first_territory.text = territories_names[0]
        btn_second_territory.text = territories_names[1]
        btn_third_territory.text = territories_names[2]
        btn_fourth_territory.text = territories_names[3]
        btn_fifth_territory.text = territories_names[4]
        btn_sixth_territory.text = territories_names[5]

        btn_first_territory.callback_data = "capture_{}".format(territories_names[0])
        btn_second_territory.callback_data = "capture_{}".format(territories_names[1])
        btn_third_territory.callback_data = "capture_{}".format(territories_names[2])
        btn_fourth_territory.callback_data = "capture_{}".format(territories_names[3])
        btn_fifth_territory.callback_data = "capture_{}".format(territories_names[4])
        btn_sixth_territory.callback_data = "capture_{}".format(territories_names[5])

        capture_territory_msg = await edit_msg.edit_text(
            text="<b>⚔ Территория</b>\n"
                 "<code>◄ Подготовка захвата. ►</code>\n\n"
                 "<i>Выберите территорию для захвата.</i>\n"
                 "▸▹▹▹",
            reply_markup=kb_capture_territories
        )
        await state.update_data({
            "capture_territory_msg": capture_territory_msg,
            "territory_name": territory_name
        })
        await Territory.capture_territory.set()

    elif callback.data == "transfer":
        pass

    elif callback.data == "camp":
        pass


@dp.callback_query_handler(state=Territory.capture_in_process)
async def capture_in_process_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")

    if callback.data == "back_menu_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup
        )
        await Territory.menu_territory.set()
        return


@dp.callback_query_handler(Regexp(regex_capture_territory), state=Territory.capture_territory)
async def capture_territory_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    territory_name = data.get("territory_name")

    if callback.data == "back_menu_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup
        )
        await Territory.menu_territory.set()
        return
    territory = re.findall(r"capture_(.*)", callback.data)[0]

    if territory == territory_name:
        await callback.answer("Нельзя захватить свою территорию.")
        return

    await edit_msg.edit_text(
        text="<b>⚔ Территория</b>\n"
             "<code>◄ Подготовка захвата. ►</code>\n\n"
             "<i>Откуда вы хотите прислать бойцов?</i>\n"
             "▸▸▹▹",
        reply_markup=kb_units_select
    )

    await state.update_data({
        "territory": territory
    })
    await Territory.select_units.set()


@dp.callback_query_handler(state=Territory.select_units)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    capture_territory_msg = data.get("capture_territory_msg")
    await state.update_data({"units_count": 0})

    if callback.data == "back_capture_territory":
        await edit_msg.edit_text(
            text=capture_territory_msg.html_text,
            reply_markup=capture_territory_msg.reply_markup
        )
        await Territory.capture_territory.set()
        return
    
    if callback.data == "camp_units":
        select_units_msg = await edit_msg.edit_text(
            text="<b>⚔ Территория</b>\n"
                 "<code>◄ Подготовка захвата. ►</code>\n\n"
                 "💂 Бойцов | 0\n\n"
                 "<i>Напишите кол-во бойцов, ответив\n"
                 "на это сообщение или выберите.</i>\n"
                 "▸▸▸▹",
            reply_markup=kb_units_count_select
        )
        await state.update_data({
            "type_units": "camp_units",
            "select_units_msg": select_units_msg
        })
        await Territory.select_count_units.set()

    elif callback.data == "base_units":
        select_units_msg = await edit_msg.edit_text(
            text="<b>⚔ Территория</b>\n"
                 "<code>◄ Подготовка захвата. ►</code>\n\n"
                 "💂 Бойцов | 0\n\n"
                 "<i>Напишите кол-во бойцов, ответив\n"
                 "на это сообщение или выберите.</i>\n"
                 "▸▸▸▹",
            reply_markup=kb_units_count_select
        )
        await state.update_data({
            "type_units": "base_units",
            "select_units_msg": select_units_msg
        })
        await Territory.select_count_units.set()


@dp.callback_query_handler(state=Territory.select_count_units)
async def count_units_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    select_units_msg = data.get("select_units_msg")

    territory = data.get("territory")
    units_count = data.get("units_count")
    territories_names = data.get("territories_names")
    territories_owners_name = data.get("territories_owners_name")
    territories_resources = data.get("territories_resources")

    territory_index = territories_names.index(territory)
    owner = territories_owners_name[territory_index]
    resource = territories_resources[territory_index]

    if callback.data == "add_one_unit":
        units_count += 1
        await state.update_data({"units_count": units_count})
    elif callback.data == "add_ten_units":
        units_count += 10
        await state.update_data({"units_count": units_count})
    elif callback.data == "add_hundred_units":
        units_count += 100
        await state.update_data({"units_count": units_count})

    elif callback.data == "capture_ready":

        if units_count == 0:
            await callback.answer(
                "Вам нужен хотя-бы 1 боец!",
                show_alert=True
            )
            return

        # если территория свободна для захвата
        if owner == "свободно":
            msg_text = read_txt_file("territory_owner_none")
            await edit_msg.edit_text(
                text=msg_text.format(
                    territory, resource_emoji[resource],
                    resource_rus[resource], units_count
                ),
                reply_markup=kb_start_capture,
            )
            await Territory.capture_free_territory.set()

        # если у территории есть владелец, начнется бой
        else:
            msg_text = read_txt_file("territory_owner")
            await edit_msg.edit_text(
                text=msg_text.format(
                    territory, resource_emoji[resource],
                    resource_rus[resource], owner, units_count
                ),
                reply_markup=kb_start_capture,
            )
            await Territory.capture_free_territory.set()

        return

    else:
        return

    await edit_msg.edit_text(
        text="<b>⚔ Территория</b>\n"
             "<code>◄ Подготовка захвата. ►</code>\n\n"
             "💂 Бойцов | {}\n\n"
             "<i>Напишите кол-во бойцов, ответив\n"
             "на это сообщение или выберите.</i>\n"
             "▸▸▸▹".format(units_count),
        reply_markup=kb_units_count_select,
    )


@dp.message_handler(IsReplyFilter(True), state=Territory.select_count_units)
# @dp.throttled(rate=1)
async def count_units_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    units_count = data.get("units_count")

    msg_text = re.findall(r"\d+", message.text)

    if not msg_text:
        await message.reply("Введи числа.")
        return

    units_count += int(message.text)
    await state.update_data({"units_count": units_count})

    await edit_msg.edit_text(
        text="<b>⚔ Территория</b>\n"
             "<code>◄ Подготовка захвата. ►</code>\n\n"
             "💂 Бойцов | {}\n\n"
             "<i>Напишите кол-во бойцов, ответив\n"
             "на это сообщение или выберите.</i>\n"
             "▸▸▸▹".format(units_count),
        reply_markup=kb_units_count_select,
    )


@dp.callback_query_handler(state=Territory.capture_free_territory)
async def count_units_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    user_id = callback.from_user.id

    if callback.data == "cancel_capture":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup
        )
        await Territory.menu_territory.set()
        return

    territory = data.get("territory")
    townhall_table = await get_townhall_table(user_id)
    territory_hash = townhall_table["territory_hash"]
    country_name = townhall_table["country_name"]

    territories_names = data.get("territories_names")
    territories_owners_name = data.get("territories_owners_name")
    territories_resources = data.get("territories_resources")
    territories_resources_emoji = data.get("territories_resources_emoji")
    type_units = data.get("type_units")
    units_count = data.get("units_count")
    territory_index = territories_names.index(territory)
    owner = territories_owners_name[territory_index]
    column = territory_db_columns[territory_index]
    resource = territories_resources[territory_index]

    if callback.data == "start_capture":
        timer = await set_timer_free_capture(user_id)

        await update_json_column(
            user_id=territory_hash,
            column=column,
            data={
                "territory": territory,
                "resource": resource,
                "owner_id": user_id,
                "owner_name": country_name,
                "units_count": units_count,
                "event": "free_capture",
            },
            table="territory"
        )

        await edit_msg.edit_text(
            text="<b>⚔ Территория</b>\n"
                 "<code>◄ Захват территории. ►</code>\n\n"
                 "Вы захватываете {}.\n\n"
                 "Захват будет окончен,"
                 "через: {}".format(territory, timer),
            reply_markup=edit_msg.reply_markup
        )
        await Territory.menu_territory.set()
        return
