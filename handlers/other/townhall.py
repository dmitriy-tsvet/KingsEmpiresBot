import states
from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.misc.read_file import read_txt_file

from utils.db_api import db_api, tables

from utils.classes import transaction, kb_constructor, timer, table_setter
from utils.ages import ages_list

from utils.ages import models


import keyboards


@dp.message_handler(chat_id=-1001316092745, state="*", commands="townhall")
async def townhall_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_mention = message.from_user.get_mention()

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    age = townhall_table.age

    # age model
    age_model: models.Age = ages_list.AgesList.get_age_model(age)

    # keyboard
    kb_townhall = kb_constructor.StandardKeyboard(user_id=user_id)
    kb_townhall = kb_townhall.create_townhall_keyboard(age)

    townhall_img = open(age_model.img, "rb")
    await message.answer_sticker(sticker=townhall_img)

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
        "index": 0
    })
    await states.Townhall.menu.set()
    session.close_session()


@dp.callback_query_handler(state=states.Townhall.menu)
async def menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    age = townhall_table.age

    citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)
    food_buildings_table: tables.FoodBuildings = session.built_in_query(tables.FoodBuildings)
    stock_buildings_table: tables.StockBuildings = session.built_in_query(tables.StockBuildings)

    # age model
    age_model = ages_list.AgesList.get_age_model(age)
    list_ages = ages_list.AgesList.get_list_ages()

    if callback.data == "progress":
        next_age = list_ages[list_ages.index(age) + 1]
        age_up_price = transaction.Transaction.get_text_price(age_model.next_age_price)

        msg_text = read_txt_file("text/townhall/progress")
        await data["edit_msg"].edit_text(
            text=msg_text.format(
                next_age,
                age_up_price
            ),
            reply_markup=keyboards.townhall.kb_progress
        )
        await states.Townhall.progress.set()

    elif callback.data == "storage":
        msg_text = read_txt_file("text/townhall/storage")
        await data["edit_msg"].edit_text(
            text=msg_text.format(
                townhall_table.food, townhall_table.stock, townhall_table.energy,
                townhall_table.graviton, townhall_table.money
            ),
            reply_markup=keyboards.townhall.kb_storage
        )
        await states.Townhall.progress.set()

    elif callback.data == "get_money":
        money_timer = timer.MoneyTimer()
        income = money_timer.get_money_timer(townhall_table, citizens_table)
        townhall_table.money += income

        await callback.answer("+ {} 💰".format(income), show_alert=False)

    elif callback.data == "get_food":
        food_timer = timer.BuildingsTimer()

        # age model
        age_model = ages_list.AgesList.get_age_model(townhall_table.age)
        building = age_model.food_building     # get food building model

        income = await food_timer.get_resource_timer(food_buildings_table, building)
        townhall_table.food += income

        await callback.answer("+ {} 🍇".format(income), show_alert=False)

    elif callback.data == "get_stock":
        stock_timer = timer.BuildingsTimer()

        # age model
        age_model = ages_list.AgesList.get_age_model(townhall_table.age)
        building = age_model.stock_building   # get stock building model

        income = await stock_timer.get_resource_timer(stock_buildings_table, building)
        townhall_table.stock += income

        await callback.answer("+ {} 🌲".format(income), show_alert=False)

    session.close_session()


@dp.callback_query_handler(state=states.Townhall.progress)
async def progress_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "back_townhall":
        await data["edit_msg"].edit_text(
            text=data["edit_msg"].html_text,
            reply_markup=data["edit_msg"].reply_markup,
        )
        await states.Townhall.menu.set()
        return

    user_id = callback.from_user.id

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    # tables data
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
    age = townhall_table.age

    # age model
    age_model = ages_list.AgesList.get_age_model(age)
    list_ages = ages_list.AgesList.get_list_ages()

    next_age = list_ages[list_ages.index(age)+1]

    if callback.data == "next_age":
        price = age_model.next_age_price

        result_transaction = transaction.Transaction.subtract_resources(
            price=price,
            townhall_table=townhall_table
        )
        price_text = transaction.Transaction.get_text_price(price)

        if result_transaction:
            next_table_age = table_setter.TableSetter(
                user_id=user_id
            )
            next_table_age.set_next_age(next_age)
            await callback.message.answer("Ты перешел в другой век!")
        else:
            await callback.answer(
                text="Переход в {} Век.\n\n"
                "Стоимость:\n"
                "{}".format(next_age, price_text),
                show_alert=True,
                cache_time=1
            )

        await callback.answer()

    session.close_session()

