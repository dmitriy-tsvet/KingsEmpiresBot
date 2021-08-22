import states
import re
from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter


from keyboards.units import kb_units, kb_about_unit, kb_creating_units,\
    btn_unit_1, btn_unit_2, btn_create_unit_1, btn_create_unit_2
from utils.misc.read_file import read_txt_file
from utils.checkers import check_user_registration
from utils.db_api.db_api2 import get_townhall_table,\
    get_units_table, update_table_data
from utils.misc.timer import set_create_unit_timer, get_time_left, set_upgrade_unit_timer

from utils.dicts import resource_emoji,\
    unit_weight_dict, age_units, units_create_timer,\
    unit_create_price, unit_upgrade_price


@dp.message_handler(chat_id=615311497, state="*", commands="units")
@dp.throttled(rate=1)
async def buildings_handler(message: types.Message, state: FSMContext):
    # data = await state.get_data()

    user_id = message.from_user.id
    user_mention = message.from_user.get_mention()

    if await check_user_registration(message, state) is True:
        return

    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]

    units_table = await get_units_table(user_id)
    upgrade_timer = units_table["upgrade_timer"]
    upgrade_unit_num = units_table["upgrade_unit_num"]
    units_count = units_table["units_count"]
    creation_queue = units_table["creation_queue"]
    creation_timer = units_table["creation_timer"]
    creation_time_left = await get_time_left(creation_timer)
    upgrade_time_left = await get_time_left(upgrade_timer)

    unit_1 = age_units[age]["unit_1"]
    unit_1_lvl = units_table["unit_1_lvl"]

    unit_2 = age_units[age]["unit_2"]
    unit_2_lvl = units_table["unit_2_lvl"]

    btn_unit_1.text = "{} ({} ур.)".format(unit_1, unit_1_lvl)
    btn_unit_1.callback_data = "about_unit_1"
    btn_create_unit_1.text = "+"
    btn_create_unit_1.callback_data = "create_unit_2"

    btn_unit_2.text = "{} ({} ур.)".format(unit_2, unit_2_lvl)
    btn_unit_2.callback_data = "about_unit_2"
    btn_create_unit_2.text = "+"
    btn_create_unit_2.callback_data = "create_unit_2"

    if upgrade_time_left > 0:
        if upgrade_unit_num == "unit_1":
            btn_unit_1.text = "✨ улучшается"
            btn_unit_1.callback_data = "None"
            btn_create_unit_1.text = "🕔"
            btn_create_unit_1.callback_data = "None"

        elif upgrade_unit_num == "unit_2":

            btn_unit_2.text = "✨ улучшается"
            btn_unit_2.callback_data = "None"
            btn_create_unit_2.text = "🕔"
            btn_create_unit_2.callback_data = "None"

    elif upgrade_time_left <= 0 and upgrade_unit_num is not None:
        await update_table_data(
            user_id=user_id,
            data={
                "upgrade_timer": 0,
                "upgrade_unit_num": None
            },
            table="units"
        )

    if creation_time_left < 1 and creation_queue > 0:
        units_count += creation_queue
        creation_queue = 0
        await update_table_data(
            user_id=user_id,
            data={
                "creation_queue": creation_queue,
                "units_count": units_count,
                "creation_timer": 0
            },
            table="units"
        )

    msg_text = read_txt_file("units/units")
    menu_msg = await message.answer(
        text=msg_text.format(units_count),
        reply_markup=kb_units
    )
    await state.update_data({
        "menu_msg": menu_msg
    })
    await states.Units.menu.set()


@dp.callback_query_handler(state=states.Units.menu)
@dp.throttled(rate=1)
async def peace_buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    menu_msg = data.get("menu_msg")
    user_id = callback.from_user.id
    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]

    units_table = await get_units_table(user_id)
    units_count = units_table["units_count"]

    about_unit = re.findall(r"about_(\w+)", callback.data)
    create_unit = re.findall(r"create_(\w+)", callback.data)

    if about_unit:
        unit_num = about_unit[0]
        unit = age_units[age][unit_num]
        unit_lvl = units_table["{}_lvl".format(unit_num)]
        unit_weight = unit_weight_dict[age][unit_num]
        units_create_time = int(units_create_timer[age][unit_num] / 60)

        msg_text = read_txt_file("about_unit")
        await menu_msg.edit_text(
            text=msg_text.format(unit, unit_lvl, units_create_time, unit_weight),
            reply_markup=kb_about_unit
        )
        await state.update_data({
            "unit_num": unit_num
        })
        return await states.Units.about_unit.set()

    elif create_unit:
        unit_num = create_unit[0]
        unit = age_units[age][unit_num]
        unit_lvl = units_table["{}_lvl".format(unit_num)]
        creation_queue = units_table["creation_queue"]
        creation_timer = units_table["creation_timer"]
        time_left = await get_time_left(creation_timer)
        if time_left < 0:
            time_left = 0

        unit_price = unit_create_price[age][unit_num]
        text_price = ""
        for i in unit_price:
            if unit_price[i] != 0:
                text_price += "{} {}".format(
                    unit_price[i], resource_emoji[i]
                )

        msg_text = read_txt_file("create_unit")
        replied_msg = await menu_msg.edit_text(
            text=msg_text.format(unit, unit_lvl, text_price, creation_queue, time_left),
            reply_markup=kb_creating_units
        )
        await state.update_data({
            "unit_num": unit_num,
            "replied_msg": replied_msg,
        })
        return await states.Units.create_unit.set()
    else:
        await callback.answer("")


@dp.callback_query_handler(state=states.Units.about_unit)
@dp.throttled(rate=1)
async def peace_buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_msg = data.get("menu_msg")

    if callback.data == "back_menu_units":
        await data["menu_msg"].edit_text(
            text=data["menu_msg"].html_text,
            reply_markup=kb_units,
        )
        await states.Units.menu.set()
        return

    user_id = callback.from_user.id
    unit_num = data.get("unit_num")

    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]
    food = townhall_table["food"]
    stock = townhall_table["stock"]
    energy = townhall_table["energy"]
    upgrade_price = unit_upgrade_price[age][unit_num]

    units_table = await get_units_table(user_id)
    upgrade_unit_num = units_table["upgrade_unit_num"]
    unit_lvl = units_table["{}_lvl".format(unit_num)]

    if callback.data == "upgrade_unit":
        if unit_lvl == 3:
            await callback.answer(
                "Уже максимальный уровень.",
                show_alert=True,
            )
            return
        elif upgrade_unit_num is not None:
            await callback.answer(
                "Нельзя прокачивать сразу 2 юнитов.",
                show_alert=True,
            )
            return

        if food < upgrade_price["food"]:
            return await callback.answer(
                "Тебе не хватает провизии."
            )
        if stock < upgrade_price["stock"]:
            return await callback.answer(
                "Тебе не хватает ресурсов."
            )
        if energy < upgrade_price["energy"]:
            return await callback.answer(
                "Тебе не хватает энергии."
            )

        food -= upgrade_price["food"]
        energy -= upgrade_price["energy"]
        stock -= upgrade_price["stock"]

        time_left = await set_upgrade_unit_timer(
            user_id=user_id,
            unit_num=unit_num
        )

        await update_table_data(
            user_id=user_id,
            data={
                "{}_lvl".format(unit_num): unit_lvl+1
            },
            table="units"
        )
        await callback.answer("Осталось {} мин.".format(time_left))

        if unit_num == "unit_1":
            btn_unit_1.text = "✨ улучшается"
            btn_unit_1.callback_data = "None"
            btn_create_unit_1.text = "🕔"
            btn_create_unit_1.callback_data = "None"

        elif unit_num == "unit_2":
            btn_unit_2.text = "✨ улучшается"
            btn_unit_2.callback_data = "None"
            btn_create_unit_2.text = "🕔"
            btn_create_unit_2.callback_data = "None"

        await data["menu_msg"].edit_text(
            text=data["menu_msg"].html_text,
            reply_markup=kb_units,
        )
        await states.Units.menu.set()


@dp.callback_query_handler(state=states.Units.create_unit)
@dp.throttled(rate=1)
async def peace_buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "back_menu_units":
        await data["menu_msg"].edit_text(
            text=data["menu_msg"].html_text,
            reply_markup=kb_units,
        )
        await states.Units.menu.set()
        return

    replied_msg = data.get("replied_msg")

    user_id = callback.from_user.id
    unit_num = data.get("unit_num")

    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]
    food = townhall_table["food"]
    stock = townhall_table["stock"]
    energy = townhall_table["energy"]
    create_price = unit_create_price[age][unit_num]

    units_table = await get_units_table(user_id)
    units_count = units_table["units_count"]
    creation_queue = units_table["creation_queue"]
    creation_timer = units_table["creation_timer"]
    time_left_min = await get_time_left(creation_timer)

    if time_left_min < 1 and creation_queue > 0:
        await callback.answer("Создано {} чел.".format(creation_queue))
        units_count += creation_queue
        creation_queue = 0
        await update_table_data(
            user_id=user_id,
            data={
                "creation_queue": creation_queue,
                "units_count": units_count,
                "creation_timer": 0
            },
            table="units"
        )

    if callback.data == "create_1_unit":

        if food < (create_price["food"] * 100):
            msg_text = read_txt_file("deficit_food")
            return await callback.answer(msg_text)
        if stock < (create_price["stock"] * 100):
            msg_text = read_txt_file("deficit_stock")
            return await callback.answer(msg_text)

        food -= (create_price["food"] * 1)
        stock -= (create_price["stock"] * 1)
        energy -= (create_price["energy"] * 1)
        creation_queue += 1
        time_left_min = await set_create_unit_timer(
            user_id=user_id,
            unit_num=unit_num,
        )

    elif callback.data == "create_10_unit":

        if food < (create_price["food"] * 100):
            msg_text = read_txt_file("deficit_food")
            return await callback.answer(msg_text)
        if stock < (create_price["stock"] * 100):
            msg_text = read_txt_file("deficit_stock")
            return await callback.answer(msg_text)

        food -= (create_price["food"] * 10)
        stock -= (create_price["stock"] * 10)
        energy -= (create_price["energy"] * 10)
        creation_queue += 10
        time_left_min = await set_create_unit_timer(
            user_id=user_id,
            unit_num=unit_num,
            units_count=10
        )

    elif callback.data == "create_100_unit":

        if food < (create_price["food"] * 100):
            msg_text = read_txt_file("deficit_food")
            return await callback.answer(msg_text)
        if stock < (create_price["stock"] * 100):
            msg_text = read_txt_file("deficit_stock")
            return await callback.answer(msg_text)

        food -= (create_price["food"] * 100)
        stock -= (create_price["stock"] * 100)
        energy -= (create_price["energy"] * 100)

        creation_queue += 100
        time_left_min = await set_create_unit_timer(
            user_id=user_id,
            unit_num=unit_num,
            units_count=100
        )

    await update_table_data(
        user_id=user_id,
        data={
            "food": food,
            "stock": stock,
            "energy": energy,
        },
        table="townhall"
    )

    await update_table_data(
        user_id=user_id,
        data={
            "creation_queue": creation_queue
        },
        table="units"
    )

    msg_text = read_txt_file("create_unit")
    await replied_msg.edit_text(
        msg_text.format(creation_queue, time_left_min)
    )


@dp.message_handler(IsReplyFilter(True), state=states.Units.create_unit)
@dp.throttled(rate=1)
async def count_units_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    replied_msg = data.get("replied_msg")

    if message.reply_to_message.message_id != replied_msg.message_id:
        return
    num_selected_units = re.findall(r"\d+", message.text)

    if not num_selected_units:
        return
    else:
        num_selected_units = int(num_selected_units[0])

    unit_num = data.get("unit_num")

    user_id = message.from_user.id
    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]
    food = townhall_table["food"]
    stock = townhall_table["stock"]
    energy = townhall_table["energy"]
    create_price = unit_create_price[age][unit_num]

    units_table = await get_units_table(user_id)
    units_count = units_table["units_count"]
    creation_queue = units_table["creation_queue"]
    creation_timer = units_table["creation_timer"]
    unit = age_units[age][unit_num]
    unit_lvl = units_table["{}_lvl".format(unit_num)]

    if food < (create_price["food"] * num_selected_units):
        units_can_make = int(food / create_price["food"])
        msg_text = "Тебе хватает только на {} 💂"
        return await message.reply(
            msg_text.format(units_can_make)
        )

    if stock < (create_price["stock"] * num_selected_units):
        units_can_make = int(food / create_price["food"])
        msg_text = "Тебе хватает только на {} 💂"
        return await message.reply(
            msg_text.format(units_can_make)
        )

    food -= (create_price["food"] * num_selected_units)
    stock -= (create_price["stock"] * num_selected_units)
    energy -= (create_price["energy"] * num_selected_units)

    creation_queue += num_selected_units
    time_left_min = await set_create_unit_timer(
        user_id=user_id,
        unit_num=unit_num,
        units_count=num_selected_units
    )

    await update_table_data(
        user_id=user_id,
        data={
            "food": food,
            "stock": stock,
            "energy": energy,
        },
        table="townhall"
    )

    await update_table_data(
        user_id=user_id,
        data={
            "creation_queue": creation_queue
        },
        table="units"
    )

    unit_price = unit_create_price[age][unit_num]
    text_price = ""
    for i in unit_price:
        if unit_price[i] != 0:
            text_price += "{} {}".format(
                unit_price[i], resource_emoji[i]
            )
            
    msg_text = read_txt_file("create_unit")
    await replied_msg.edit_text(
        msg_text.format(unit, unit_lvl, unit_create_price, creation_queue, time_left_min)
    )
