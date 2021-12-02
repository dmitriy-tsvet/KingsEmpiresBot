import random
from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.misc.read_file import read_txt_file

from utils.db_api import db_api, tables

from utils.classes import transaction, kb_constructor, regexps
from utils.models import ages

import re
import keyboards


@dp.message_handler(state="*", commands="shop")
async def shop_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    if message.chat.type != "private":
        await message.reply(
            text="💠 Магазин доступен в лс.",
            reply_markup=keyboards.shop.kb_url_private_chat
        )
        return

    shop_msg = await message.answer(
        text="Магазин",
        reply_markup=keyboards.shop.kb_shop
    )

    await state.update_data({
        "user_id": user_id,
        "shop_msg": shop_msg
    })


@dp.callback_query_handler(state="*", regexp=regexps.ShopRegexp.back)
async def shop_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    shop_msg: types.Message = data.get("shop_msg")
    chest_msg: types.Message = data.get("chest_msg")

    if callback.data == "back_shop":
        await shop_msg.edit_text(
            text=shop_msg.html_text,
            reply_markup=shop_msg.reply_markup
        )
    elif callback.data == "back_chest":
        await shop_msg.edit_text(
            text=chest_msg.html_text,
            reply_markup=chest_msg.reply_markup
        )


@dp.callback_query_handler(state="*", regexp=regexps.ShopRegexp.menu)
async def shop_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    shop_msg: types.Message = data.get("shop_msg")

    session = db_api.CreateSession()
    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    if callback.data == "shop_chest":
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_shop_chest_keyboard()
        msg_text = read_txt_file("text/shop/shop_money")
        chest_msg = await shop_msg.edit_text(
            text="Сундуки",
            reply_markup=keyboard
        )
        await state.update_data({
            "chest_msg": chest_msg
        })

    elif callback.data == "shop_money":

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_shop_money_keyboard()
        msg_text = read_txt_file("text/shop/shop_money")
        await shop_msg.edit_text(
            text=msg_text.format(townhall.money, townhall.diamonds),
            reply_markup=keyboard
        )
    elif callback.data == "shop_stock":
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_shop_stock_keyboard()
        msg_text = read_txt_file("text/shop/shop_stock")
        await shop_msg.edit_text(
            text=msg_text.format(townhall.stock, townhall.diamonds),
            reply_markup=keyboard
        )
    elif callback.data == "shop_donate":
        msg_text = read_txt_file("text/shop/shop_donate")
        await shop_msg.edit_text(
            text=msg_text.format(townhall.stock, townhall.diamonds),
            reply_markup=keyboards.shop.kb_donate
        )

    session.close()


@dp.callback_query_handler(state="*", regexp=regexps.ShopRegexp.buy)
async def shop_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    shop_msg: types.Message = data.get("shop_msg")

    session = db_api.CreateSession()
    townhall: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    progress: tables.Progress = session.filter_by_user_id(
        user_id=user_id, table=tables.Progress)

    buildings: tables.Buildings = session.filter_by_user_id(
        user_id=user_id, table=tables.Buildings)

    if re.findall(r"get_chest_(\d+)", callback.data):
        chest_num = re.findall(r"get_chest_(\d+)", callback.data)
        chest_num = int(chest_num[0])

        chests = ages.Age.get_all_chests()
        chest = chests[chest_num]

        text = ""
        for i in enumerate(chest.content):
            index = i[0]
            value = i[1]

            chance = chest.chances[index]
            if value == "diamonds":
                text += "▸ <i>💎 Кристаллы ({}%)</i>\n".format(chance)
            elif value == "money":
                text += "▸ <i>💰 Монеты ({}%)</i>\n".format(chance)
            elif value == "stock":
                text += "▸ <i>⚒ Ресурсы ({}%)</i>\n".format(chance)
            elif value == "score":
                text += "▸ <i>🧬 Очки Науки ({}%)</i>\n".format(chance)
            elif value == "builder_home":
                text += "▸ <i>🪚🏠 Дом Строитлея ({}%)</i>\n".format(chance)
            elif value == "land":
                text += "▸ <i>🌲 Земли ({}%)</i>\n".format(chance)

        msg_text = read_txt_file("text/shop/shop_chest")
        chest_price = chest.price[:]
        await shop_msg.edit_text(
            text=msg_text.format(chest.name, transaction.Purchase.get_price(chest_price), text),
            reply_markup=keyboards.shop.kb_buy_chest
        )
        await state.update_data({"chest_num": chest_num})

    elif callback.data == "buy_chest":
        chest_num = data.get("chest_num")
        if chest_num is None:
            return

        chests = ages.Age.get_all_chests()
        chest = chests[chest_num]
        chest_price = chest.price[:]
        buying = transaction.Purchase.buy(chest_price, townhall)
        if buying:
            value = random.choices(population=chest.content, weights=chest.chances)[0]
            index = chest.content.index(value)
            count = chest.counts[index]

            text = ""
            if value == "diamonds":
                count = random.randint(*count)
                text += "+ {} 💎 Кристаллы".format(count)
                townhall.diamonds += count
            elif value == "money":
                count = random.randint(*count)
                text += "+ {} 💰 Монеты".format(count)
                townhall.money += count
            elif value == "stock":
                count = random.randint(*count)
                text += "+ {} ⚒ Ресурсы".format(count)
                townhall.stock += count
            elif value == "score":
                count = random.randint(*count)
                text += "+ {} 🧬 Очки Науки".format(count)
                progress.score += count
            elif value == "builder_home":
                buildings_buildings = list(buildings.buildings)
                if buildings_buildings[0] != 0:
                    buildings_buildings[0] = 0
                    buildings.buildings = buildings_buildings
                    text += "+ 🪚🏠 Дом Строителя\n"
                else:
                    buildings.buildings = buildings_buildings
                    text += "+ 🪚🏠 Дом Строителя\n\n" \
                            "<i>Вы уже выбивали дом строителя,\n" \
                            "он не будет построен.</i>"
            elif value == "land":
                count = random.randint(*count)
                lands = ["tree" for i in range(0, count)]
                buildings.buildings += lands
                text += "+ {} 🌲 Земли".format(count)

            await callback.message.answer("🔐")
            await callback.message.reply(
                "<b>Вы открываете {}.</b>\n"
                "{}".format(chest.name, text)
            )
            await callback.answer(text)
        else:
            chest_price = chest.price[:]
            price = transaction.Purchase.get_dynamic_price(chest_price, townhall)
            await callback.answer("Вам не хватает {}".format(price))

    elif re.findall(r"shop_buy_money_(\d+)_for_(\d+)", callback.data):
        money_value = re.findall(r"_(\d+)_", callback.data)
        money_value = int(money_value[0])
        diamonds_value = re.findall(r"for_(\d+)", callback.data)
        diamonds_value = int(diamonds_value[0])

        if townhall.diamonds >= diamonds_value:
            townhall.diamonds -= diamonds_value
            townhall.money += money_value
            await callback.answer("+{} 💰".format(money_value))

            keyboard = kb_constructor.StandardKeyboard(
                user_id=user_id).create_shop_money_keyboard()
            msg_text = read_txt_file("text/shop/shop_money")
            await shop_msg.edit_text(
                text=msg_text.format(townhall.money, townhall.diamonds),
                reply_markup=keyboard
            )
        else:
            await callback.answer("Тебе не хватает {} 💎".format(
                diamonds_value - townhall.diamonds
            ))

    elif re.findall(r"shop_buy_stock_(\d+)_for_(\d+)", callback.data):
        stock_value = re.findall(r"_(\d+)_", callback.data)
        stock_value = int(stock_value[0])
        diamonds_value = re.findall(r"for_(\d+)", callback.data)
        diamonds_value = int(diamonds_value[0])

        if townhall.diamonds >= diamonds_value:
            townhall.diamonds -= diamonds_value
            townhall.stock += stock_value
            await callback.answer("+{} ⚒".format(stock_value))

            keyboard = kb_constructor.StandardKeyboard(
                user_id=user_id).create_shop_stock_keyboard()
            msg_text = read_txt_file("text/shop/shop_stock")
            await shop_msg.edit_text(
                text=msg_text.format(townhall.stock, townhall.diamonds),
                reply_markup=keyboard
            )
        else:
            await callback.answer("Тебе не хватает {} 💎".format(
                diamonds_value - townhall.diamonds
            ))

    await callback.answer()
    session.close()
