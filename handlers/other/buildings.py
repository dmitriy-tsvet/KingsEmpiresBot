import states
import re
import json
import random

from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.misc.read_file import read_txt_file
from utils.db_api import tables, db_api
from utils.ages import ages_list, models
from utils.classes import kb_constructor, timer

import keyboards


@dp.message_handler(chat_id=-1001316092745, state="*", commands="buildings")
async def buildings_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    age = townhall_table.age

    keyboard = kb_constructor.StandardKeyboard(
        user_id=user_id
    )
    keyboard = keyboard.create_buildings_keyboard(age)

    buildings_msg = await message.answer(
        text="<b>Здания </b>\n\n"
             "<i>Прокачивайте здания,\n"
             "для более высокой\n"
             "производительности.</i>",
        reply_markup=keyboard
    )

    session.close_session()

    await state.set_data({
        "buildings_msg": buildings_msg
    })
    await states.Buildings.menu.set()


@dp.callback_query_handler(state=states.Buildings.menu)
async def buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    buildings_msg = data.get("buildings_msg")

    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)
    age = townhall_table.age

    # model of age
    age_model: models.Age = ages_list.AgesList.get_age_model(age)

    keyboard = kb_constructor.StandardKeyboard(
        user_id=user_id
    )

    type_buildings = re.findall(r"(\w+)_buildings", callback.data)

    if callback.data == "home_buildings":
        keyboard = keyboard.create_homes_keyboard()

        msg_text = read_txt_file("text/buildings/homes")
        await buildings_msg.edit_text(
            text=msg_text.format(
                citizens_table.population,
                citizens_table.capacity,
                age_model.home_building.name,
                citizens_table.home_counts,
            ),
            reply_markup=keyboard
        )
        await states.Buildings.home_buildings.set()

    elif type_buildings:
        type_building = str(type_buildings[0])

        if type_building == "food":
            some_buildings_table: tables.FoodBuildings = session.built_in_query(
                tables.FoodBuildings
            )

            building_model = age_model.food_building
            keyboard = keyboard.create_some_buildings_keyboard(
                table_model=tables.FoodBuildings,
                building_model=building_model
            )
            emoji = "🍇"

        elif type_building == "stock":
            some_buildings_table: tables.StockBuildings = session.built_in_query(
                tables.StockBuildings
            )
            building_model = age_model.stock_building
            keyboard = keyboard.create_some_buildings_keyboard(
                table_model=tables.StockBuildings,
                building_model=building_model
            )
            emoji = "🌲"

        else:
            some_buildings_table = None
            building_model = None
            emoji = None

        if building_model is None:
            session.close_session()

            return await callback.answer(
                text="Слишком маленький век.",
                show_alert=True
            )

        msg_text = read_txt_file("text/buildings/about_buildings")
        efficiency = building_model.get_all_efficiency(some_buildings_table)
        some_buildings_msg = await buildings_msg.edit_text(
            text=msg_text.format(
                building_model.name,
                emoji, efficiency,
                some_buildings_table.count_buildings
            ),
            reply_markup=keyboard
        )

        await state.update_data({
            "building_model": building_model,
            "type_building": type_building,
            "some_buildings_msg": some_buildings_msg,
        })
        await states.Buildings.some_buildings.set()

    session.close_session()
    await callback.answer("")


@dp.callback_query_handler(state=states.Buildings.home_buildings)
async def home_buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "back_buildings":
        await data["buildings_msg"].edit_text(
            text=data["buildings_msg"].html_text,
            reply_markup=data["buildings_msg"].reply_markup,
        )
        await states.Buildings.menu.set()
        return

    user_id = callback.from_user.id
    add_home = re.findall(r"add_home_(\d+)", callback.data)
    build_time = re.findall(r"home_build_time", callback.data)

    session = db_api.Session(user_id=user_id)

    if add_home:
        session.open_session()

        townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
        citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)

        age_model = ages_list.AgesList.get_age_model(townhall_table.age)

        building_model = age_model.home_building

        num_building = int(add_home[0])
        create_price = building_model.create_price

        if townhall_table.money >= create_price:
            time_left = timer.Timer.get_left_time(citizens_table.build_timer)

            if time_left[0] > 0:
                session.close_session()
                return await callback.answer(
                    text="уже идет стройка",
                )

            townhall_table.money -= create_price

            citizens_table.build_num = num_building
            citizens_table.home_counts += 1
            timer.Timer.set_build_timer(citizens_table, building_model)

            await data["buildings_msg"].edit_text(
                text=data["buildings_msg"].html_text,
                reply_markup=data["buildings_msg"].reply_markup,
            )
            await states.Buildings.menu.set()
        else:
            await callback.answer(
                "Стоимость:\n"
                "{} 💰".format(create_price),
                show_alert=True,
            )

    elif build_time:
        citizens_table = session.quick_session(tables.Citizens)

        time_left = timer.Timer.get_left_time(citizens_table.build_timer)
        await callback.answer(
            text="⏱ Осталось: {} {}".format(*time_left),
            cache_time=1
        )
    else:
        people_dialogs = [
            "а? кто там?", "пенсия наверно пришла",
            "не стучите! я занят!", "мам, там кто-то стучит!",
            "интересно, а что если я в игре?",
            "ёлки-палки, опять штраф что-ли", "*тишина*",
            "Гарри, это ты?", "хмм, кому я вдруг понадобился"
        ]
        random_dialog = random.choice(people_dialogs)
        random_dialog = "💭 {}".format(random_dialog)

        await callback.answer(
            text=random_dialog,
            cache_time=1
        )
    session.close_session()
    await callback.answer()


@dp.callback_query_handler(state=states.Buildings.some_buildings)
async def some_buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "back_buildings":
        await data["buildings_msg"].edit_text(
            text=data["buildings_msg"].html_text,
            reply_markup=data["buildings_msg"].reply_markup,
        )
        await states.Buildings.menu.set()
        return

    user_id = callback.from_user.id
    buildings_msg = data.get("buildings_msg")
    type_building = data.get("type_building")
    building_model = data.get("building_model")

    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    age = townhall_table.age

    selected_building = re.findall(r"check_{}_building_(\d)".format(type_building), callback.data)
    add_building = re.findall(r"add_{}_building_(\d)".format(type_building), callback.data)

    if type_building == "food":
        some_buildings: tables.FoodBuildings = session.built_in_query(tables.FoodBuildings)
        emoji = "🍇"
    else:
        some_buildings: tables.StockBuildings = session.built_in_query(tables.StockBuildings)
        emoji = "🌲"

    if selected_building:
        num_building = int(selected_building[0])

        # model of age
        levels = list(some_buildings.levels)

        msg_text = read_txt_file("text/buildings/about_building")
        await buildings_msg.edit_text(
            text=msg_text.format(
                building_model.name,
                levels[num_building],
                emoji,
                building_model.get_hour_efficiency(levels[num_building])
            ),
            reply_markup=keyboards.buildings.kb_about_building
        )

        await state.update_data({
            "num_building": num_building,
        })
        await states.Buildings.about_building.set()

    elif add_building:
        num_building = int(add_building[0])

        create_price = building_model.create_price

        if townhall_table.money >= create_price:
            time_left_build = timer.Timer.get_left_time(some_buildings.build_timer)

            if time_left_build[0] > 0:
                session.close_session()
                return await callback.answer(
                    text="уже идет стройка",
                )

            townhall_table.money -= create_price

            some_buildings.build_num = num_building
            some_buildings.count_buildings += 1
            timer.Timer.set_build_timer(some_buildings, building_model)

            await data["buildings_msg"].edit_text(
                text=data["buildings_msg"].html_text,
                reply_markup=data["buildings_msg"].reply_markup,
            )
            await states.Buildings.menu.set()
        else:
            await callback.answer(
                "Стоимость:\n"
                "{} 💰".format(create_price),
                show_alert=True,
            )

    session.close_session()
    await callback.answer("")


@dp.callback_query_handler(state=states.Buildings.about_building)
async def about_building_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "back_some_buildings":
        await data["buildings_msg"].edit_text(
            text=data["some_buildings_msg"].html_text,
            reply_markup=data["some_buildings_msg"].reply_markup,
        )
        await states.Buildings.some_buildings.set()
        return

    user_id = callback.from_user.id

    if callback.data == "upgrade_building":
        session = db_api.Session(user_id=user_id)
        session.open_session()

        num_building: int = data.get("num_building")
        building_model: models.Building = data.get("building_model")
        type_building: str = data.get("type_building")

        townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)

        if type_building == "food":
            some_buildings: tables.FoodBuildings = session.built_in_query(tables.FoodBuildings)
        else:
            some_buildings: tables.StockBuildings = session.built_in_query(tables.StockBuildings)

        levels = list(some_buildings.levels)
        current_building_lvl = levels[num_building]

        if current_building_lvl == 5:
            await callback.answer(
                "Уже максимальный уровень.",
                show_alert=True,
            )
            session.close_session()
            return

        upgrade_price = building_model.upgrade_price

        if townhall_table.money >= upgrade_price:
            time_left_build = timer.Timer.get_left_time(some_buildings.build_timer)

            if time_left_build[0] > 0:
                session.close_session()
                return await callback.answer(
                    text="уже идет стройка",
                )

            townhall_table.money -= upgrade_price
            some_buildings.build_num = num_building

            set_time = timer.Timer.set_timer(building_model.upgrade_time_sec)
            some_buildings.build_timer = set_time

            await data["buildings_msg"].edit_text(
                text=data["buildings_msg"].html_text,
                reply_markup=data["buildings_msg"].reply_markup,
            )
            await states.Buildings.menu.set()

        else:
            await callback.answer(
                "Стоимость:\n"
                "{} 💰".format(upgrade_price),
                show_alert=True,
            )

        session.close_session()
