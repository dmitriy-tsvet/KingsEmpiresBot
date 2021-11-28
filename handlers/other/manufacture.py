import typing

import keyboards
import states
import re
import copy
import random
import time

from loader import dp
from aiogram import types
from aiogram.dispatcher import filters
from aiogram import exceptions

from aiogram.dispatcher import FSMContext
from utils.db_api import tables, db_api
from utils.models import ages
from utils.classes import kb_constructor, timer
from utils.models import base
from utils.misc.regexps import ManufactureRegexp
from utils.misc.read_file import read_txt_file

from data import config


@dp.message_handler(state="*", commands="manufacture")
async def territory_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    session = db_api.CreateSession()

    manufacture: tables.Manufacture = session.db.query(
        tables.Manufacture).filter_by(user_id=user_id).first()

    timer.ManufactureTimer().get_creation_queue(user_id=user_id)

    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id).create_manufacture_keyboard()

    if not keyboard.inline_keyboard:
        msg_text = read_txt_file("text/manufacture/not_manufacture")
        manufacture_msg = await message.reply(
            text=msg_text
        )
    else:
        msg_text = read_txt_file("text/manufacture/manufacture")
        manufacture_msg = await message.reply(
            text=msg_text,
            reply_markup=keyboard
        )

    await state.update_data(
        await state.update_data({
            "user_id": user_id,
            "manufacture_msg": manufacture_msg,
        })
    )
    session.close()


@dp.callback_query_handler(regexp=ManufactureRegexp.back)
async def callback_handler2(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        return await callback.answer("Не трогай чужое!")

    manufacture_msg: types.Message = data.get("manufacture_msg")
    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id).create_manufacture_keyboard()

    msg_text = read_txt_file("text/manufacture/manufacture")
    await manufacture_msg.edit_text(
        text=msg_text,
        reply_markup=keyboard
    )
    await callback.answer()


@dp.callback_query_handler(regexp=ManufactureRegexp.menu)
async def callback_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        return await callback.answer("Не трогай чужое!")

    manufacture_msg: types.Message = data.get("manufacture_msg")

    building_manufacture_pos = re.findall(r"building_manufacture_pos_(\d+)", callback.data)
    create_product = re.findall(r"create_product_(\d+)", callback.data)
    get_product = re.findall(r"manufacture_product_(\d+)", callback.data)

    session = db_api.CreateSession()

    # tables data
    manufacture: tables.Manufacture = session.db.query(
        tables.Manufacture).filter_by(user_id=user_id).first()

    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()

    all_buildings = ages.Age.get_all_buildings()
    all_products = ages.Age.get_all_products()

    if building_manufacture_pos:
        building_pos = int(building_manufacture_pos[0])
        building: base.ManufactureBuilding = all_buildings[buildings.buildings[building_pos]]

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_manufacture_products_keyboard(manufacture_building=building)

        msg_text = read_txt_file("text/manufacture/create_product")
        products_txt = ""
        for product in building.products:
            products_txt += "{} - {} ⚒ / {} {}\n".format(
                product.name,
                product.income,
                *timer.Timer.get_left_time(int(product.create_time_sec+time.time()))
            )
            if product != building.products[-1]:
                products_txt += "⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n"

        await manufacture_msg.edit_text(
            text=msg_text.format(
                building.name,
                products_txt
            ),
            reply_markup=keyboard
        )
        await state.update_data({
            "building_manufacture_pos": building_pos
        })
    elif create_product:
        product_id = int(create_product[0])
        product: base.ManufactureProduct = all_products[product_id]
        building_pos = data.get("building_manufacture_pos")
        if building_pos is None:
            await callback.answer()
            session.close()
            return

        creation_queue = list(manufacture.creation_queue)

        creation_queue_buildings = [i["building_pos"] for i in creation_queue]
        if building_pos not in creation_queue_buildings:
            creation_queue.append({
                "product_id": product_id,
                "timer": timer.Timer.set_timer(product.create_time_sec),
                "building_pos": building_pos
            })

        if not creation_queue:
            creation_queue.append({
                "product_id": product_id,
                "timer": timer.Timer.set_timer(product.create_time_sec),
                "building_pos": building_pos
            })

        manufacture.creation_queue = creation_queue
        session.db.commit()

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_manufacture_keyboard()

        await manufacture_msg.edit_text(
            text=manufacture_msg.html_text,
            reply_markup=keyboard
        )

    elif get_product:
        product_id = int(get_product[0])
        timer.ManufactureTimer().get_wait_queue(user_id=user_id, product_id=product_id)

        product: base.ManufactureProduct = all_products[product_id]
        product_emoji = re.findall(r"(\W+)\s+", product.name)[0]
        text = "+1 {}".format(product_emoji)

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_manufacture_keyboard()
        await manufacture_msg.edit_text(
            text=manufacture_msg.html_text,
            reply_markup=keyboard
        )
        await callback.answer(text)

    session.close()
