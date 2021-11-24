import states
import re
import random
import typing

from loader import dp
from data import config

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from utils.misc.read_file import read_txt_file
from utils.misc.regexps import BuildingsRegexp
from utils.db_api import tables, db_api
from utils.models import ages, base, buildings_territory, clan_building
from utils.classes import kb_constructor, timer, transaction

import keyboards


@dp.message_handler(state="*", commands="buildings")
async def buildings_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    session = db_api.CreateSession()

    # tables data
    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    buildings: tables.Buildings = session.filter_by_user_id(
        user_id=user_id, table=tables.Buildings)

    timer.BuildingTimer().get_build_timer(user_id=user_id)

    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id).create_buildings_keyboard()
    # building_img = random.choice(age_model.buildings_img)

    # with open("data/img/buildings/{}.webp".format(building_img), 'rb') as sticker:
    #     await message.answer_sticker(sticker=sticker)

    msg_text = read_txt_file("text/buildings/buildings")
    buildings_msg = await message.answer(
        text=msg_text.format(
            buildings.buildings.count(0)-len(buildings.build_timer),
            buildings.buildings.count(0)),
        reply_markup=keyboard
    )

    session.close()

    await state.update_data({
        "user_id": user_id,
        "buildings_msg": buildings_msg
    })
    # await states.Buildings.menu.set()


@dp.callback_query_handler(state="*", regexp=BuildingsRegexp.back)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    buildings_msg: types.Message = data.get("buildings_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    if callback.data == "back_buildings":
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_buildings_keyboard()
        await buildings_msg.edit_text(
            text=buildings_msg.html_text,
            reply_markup=keyboard,
        )
    await callback.answer()


@dp.callback_query_handler(regexp=BuildingsRegexp.building)
async def buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    buildings_msg: types.Message = data.get("buildings_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()

    page_move = re.findall(r"building_page_(\d+)", callback.data)
    building_pos = re.findall(r"building_pos_(\d+)", callback.data)
    build_info = re.findall(r"build_info_(\d+)", callback.data)

    base_buildings: typing.List[typing.Union[
        base.BuilderHome, base.StockBuilding, base.ClanBuilding,
        base.ManufactureBuilding, base.HomeBuilding
    ]] = ages.Age.get_all_buildings()

    if page_move:
        page = int(page_move[0])

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_buildings_keyboard(page)
        try:
            await buildings_msg.edit_reply_markup(
                reply_markup=keyboard
            )
        except exceptions.MessageNotModified:
            pass

    elif building_pos:
        position = int(building_pos[0])

        await state.update_data({
            "build_pos": position
        })

        if buildings.buildings[position] is None:
            # нужно говорить юзеру, если у него нету зданий
            keyboard = kb_constructor.PaginationKeyboard(
                user_id=user_id).create_unlocked_buildings_keyboard()

            await buildings_msg.edit_text(
                text="Постройка здания\n",
                reply_markup=keyboard
            )
        else:
            building = base_buildings[buildings.buildings[position]]
            name = building.name

            if type(building) is base.ManufactureBuilding:
                text = ""
                for i in building.products:
                    text += "<i>- {}</i>\n".format(i.name)
                msg_text = read_txt_file("text/buildings/manufacture_building")
                await buildings_msg.edit_text(
                    text=msg_text.format(name, building, text),
                    reply_markup=keyboards.buildings.kb_back
                )
            elif type(building) is base.StockBuilding:
                msg_text = read_txt_file("text/buildings/stock_building")
                await buildings_msg.edit_text(
                    text=msg_text.format(name, building, building.efficiency),
                    reply_markup=keyboards.buildings.kb_back
                )

            elif type(building) is base.HomeBuilding:
                msg_text = read_txt_file("text/buildings/home_building")
                await buildings_msg.edit_text(
                    text=msg_text.format(name, building, building.capacity, building.income),
                    reply_markup=keyboards.buildings.kb_back
                )

            elif type(building) is base.BuilderHome:
                msg_text = read_txt_file("text/buildings/builder_home")
                await buildings_msg.edit_text(
                    text=msg_text.format(name, building),
                    reply_markup=keyboards.buildings.kb_back
                )

            elif type(building) is base.ClanBuilding:
                if buildings.clan_building_lvl == 0:
                    msg_text = read_txt_file("text/buildings/clan_destroy")
                    await buildings_msg.edit_text(
                        text=msg_text,
                        reply_markup=keyboards.buildings.kb_fix_clan_building
                    )

                elif buildings.clan_building_lvl > 0:
                    msg_text = read_txt_file("text/buildings/clan_not_destroy")
                    keyboard = kb_constructor.StandardKeyboard(
                        user_id=user_id).create_upgrade_clan_keyboard()
                    await buildings_msg.edit_text(
                        text=msg_text.format(
                            buildings.clan_building_lvl,
                            clan_building.clan_building.capacity * buildings.clan_building_lvl
                        ),
                        reply_markup=keyboard
                    )

            else:
                msg_text = read_txt_file("text/buildings/builder_home")
                await buildings_msg.edit_text(
                    text=msg_text.format(name),
                    reply_markup=keyboards.buildings.kb_back
                )

    elif build_info:
        build_num = int(build_info[0])
        if data.get("build_pos") is None:
            return
        building = base_buildings[build_num]

        build_time = timer.Timer.get_left_time_min(building.create_time_sec)
        build_price = transaction.Purchase.get_price(building.create_price)

        if type(building) is base.ManufactureBuilding:
            text = ""
            for i in building.products:
                if building.products.index(i) == len(building.products)-1:
                    text += "<i>{}</i>".format(i.name)
                    break
                text += "<i>{} / </i>".format(i.name)

            msg_text = read_txt_file("text/buildings/pre_build_manufacture")
            await buildings_msg.edit_text(
                text=msg_text.format(
                    building.name, building, text, build_price, building.manpower, *build_time),
                reply_markup=keyboards.buildings.kb_build_info)

        elif type(building) is base.StockBuilding:
            msg_text = read_txt_file("text/buildings/pre_build_stock")
            await buildings_msg.edit_text(
                text=msg_text.format(
                    building.name, building, building.efficiency, build_price, building.manpower, *build_time),
                reply_markup=keyboards.buildings.kb_build_info)

        elif type(building) is base.HomeBuilding:
            msg_text = read_txt_file("text/buildings/pre_build_home")
            await buildings_msg.edit_text(
                text=msg_text.format(
                    building.name, building, building.capacity, building.income, build_price, *build_time),
                reply_markup=keyboards.buildings.kb_build_info)
        else:
            create_price = building.create_price
            if type(building) is base.BuilderHome:
                create_price = [i*buildings.buildings.count(0) for i in create_price]

            create_price = transaction.Purchase.get_price(create_price)
            msg_text = read_txt_file("text/buildings/pre_build")
            await buildings_msg.edit_text(
                text=msg_text.format(
                    building.name, building, create_price, *build_time),
                reply_markup=keyboards.buildings.kb_build_info)

        await state.update_data({
            "build_num": build_num
        })

    elif callback.data == "start_build":
        if data.get("build_pos") is None:
            await callback.answer()
            session.close()
            return
        elif data.get("build_num") is None:
            await callback.answer()
            session.close()
            return

        build_num = int(data.get("build_num"))
        build_pos = int(data.get("build_pos"))
        building = base_buildings[build_num]
        create_price = building.create_price
        if type(building) is base.BuilderHome:
            create_price *= buildings.buildings.count(0)

        buying = transaction.Purchase.buy(
            price=create_price,
            townhall=townhall
        )

        if not buying:
            price = transaction.Purchase.get_dynamic_price(
                price=create_price,
                townhall=townhall
            )
            msg_text = read_txt_file("text/hints/few_money")
            await callback.answer(
                text=msg_text.format(price)
            )
            session.close()
            return
        if type(base_buildings[build_num]) in (base.StockBuilding, base.ManufactureBuilding):
            if townhall.population >= base_buildings[build_num].manpower:
                townhall.population -= base_buildings[build_num].manpower
            else:
                manpower = base_buildings[build_num].manpower
                await callback.answer(
                    text="Вам не хватает x{} 👨🏼‍🌾 Жителей".format(
                        manpower - townhall.population
                    )
                )
                session.close()
                return

        build_timer = list(buildings.build_timer)
        build_timer.append(
            {"timer": timer.Timer.set_timer(base_buildings[build_num].create_time_sec),
             "build_num": build_num,
             "build_pos": build_pos
             }
        )

        if buildings.buildings.count(0) > len(buildings.build_timer):
            buildings.build_timer = build_timer
            session.db.commit()

            keyboard = kb_constructor.PaginationKeyboard(
                user_id=user_id).create_buildings_keyboard()
            msg_text = read_txt_file("text/buildings/buildings")
            await buildings_msg.edit_text(
                text=msg_text.format(
                    buildings.buildings.count(0) - len(buildings.build_timer),
                    buildings.buildings.count(0)),
                reply_markup=keyboard
            )

        else:
            await callback.answer("Все строители заняты.")

    await callback.answer()
    session.close()


@dp.callback_query_handler(regexp=BuildingsRegexp.clan_building)
async def buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    buildings_msg: types.Message = data.get("buildings_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()

    page_move = re.findall(r"building_page_(\d+)", callback.data)
    building_pos = re.findall(r"building_pos_(\d+)", callback.data)
    build_info = re.findall(r"build_info_(\d+)", callback.data)

    base_buildings: typing.List[typing.Union[
        base.BuilderHome, base.StockBuilding, base.ClanBuilding,
        base.ManufactureBuilding
    ]] = ages.Age.get_all_buildings()

    if callback.data == "fix_clan_building":
        buying = transaction.Purchase.buy(
            price=clan_building.clan_building.fix_price, townhall=townhall
        )

        if buying:
            buildings.clan_building_lvl = 1

            await buildings_msg.edit_text(
                text=buildings_msg.html_text,
                reply_markup=buildings_msg.reply_markup,
            )
            await callback.answer("🔨 Клановая крепость построена.")
        else:
            fix_price = transaction.Purchase.get_dynamic_price(
                price=clan_building.clan_building.fix_price, townhall=townhall
            )
            await callback.answer("Вам не хватает {}".format(fix_price))

    elif callback.data == "upgrade_clan_building":
        upgrade_price = [i*buildings.clan_building_lvl for i in clan_building.clan_building.upgrade_price]
        buying = transaction.Purchase.buy(
            price=upgrade_price, townhall=townhall
        )

        if buying:
            buildings.clan_building_lvl += 1
            await buildings_msg.edit_text(
                text=buildings_msg.html_text,
                reply_markup=buildings_msg.reply_markup,
            )
            await callback.answer("🔨 Клановая крепость улучшена.")
        else:
            upgrade_price = transaction.Purchase.get_dynamic_price(
                price=upgrade_price, townhall=townhall
            )

            await callback.answer("Вам не хватает {}".format(upgrade_price))

    await callback.answer()
    session.close()


@dp.callback_query_handler(regexp=BuildingsRegexp.unlocked_buildings)
async def buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    buildings_msg: types.Message = data.get("buildings_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()

    page_move = re.findall(r"unlocked_buildings_page_(\d+)", callback.data)

    base_buildings: typing.List[typing.Union[
        base.BuilderHome, base.StockBuilding, base.ClanBuilding,
        base.ManufactureBuilding
    ]] = ages.Age.get_all_buildings()

    if page_move:
        page = int(page_move[0])
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_unlocked_buildings_keyboard(page)

        try:
            await buildings_msg.edit_reply_markup(
                reply_markup=keyboard
            )
        except exceptions.MessageNotModified:
            pass

    session.close()
    await callback.answer()


@dp.callback_query_handler(regexp=BuildingsRegexp.tree)
async def buildings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    buildings_msg: types.Message = data.get("buildings_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    # tables data
    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()

    tree_pos = re.findall(r"tree_pos_(\d+)", callback.data)

    base_buildings: typing.List[typing.Union[
        base.BuilderHome, base.StockBuilding, base.ClanBuilding,
        base.ManufactureBuilding
    ]] = ages.Age.get_all_buildings()

    if tree_pos:
        pos = int(tree_pos[0])
        await buildings_msg.edit_text(
            text="🌲 Дерево\n"
                 "<i>Просто деревцо, срубив\n"
                 "которое вы получите место\n"
                 "для новой постройки.</i>",
            reply_markup=keyboards.buildings.kb_tree
        )
        await state.update_data({
            "tree_pos": pos
        })

    elif callback.data == "cut_down":
        if data.get("tree_pos") is None:
            session.close()
            return
        crnt_buildings = list(buildings.buildings)
        build_timer = list(buildings.build_timer)
        cut_down_time = random.randint(360, 1380)

        build_timer.append(
            {"timer": timer.Timer.set_timer(cut_down_time),
             "build_pos": data.get("tree_pos")
             })

        if buildings.buildings.count(0) > len(buildings.build_timer):
            buildings.build_timer = build_timer
            session.db.commit()

            keyboard = kb_constructor.PaginationKeyboard(
                user_id=user_id).create_buildings_keyboard()

            msg_text = read_txt_file("text/buildings/buildings")
            await buildings_msg.edit_text(
                text=msg_text.format(
                    buildings.buildings.count(0) - len(buildings.build_timer),
                    buildings.buildings.count(0)),
                reply_markup=keyboard
            )

        else:
            await callback.answer("Все строители заняты.")
            session.close()
            return

        crnt_buildings[data.get("tree_pos")] = None
        buildings.buildings = crnt_buildings

    await callback.answer()
    session.close()
