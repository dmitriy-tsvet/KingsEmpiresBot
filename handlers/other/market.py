from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from utils.misc.read_file import read_txt_file

from utils.classes import kb_constructor, timer, regexps
from utils.db_api import db_api, tables
from utils.models import ages

import re


@dp.message_handler(state="*", commands="market")
async def market_command_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id).create_market_keyboard()

    msg_text = read_txt_file("text/market/list_products")
    market_msg = await message.answer(
        msg_text.format(1, keyboard[1]),
        reply_markup=keyboard[0]
    )

    await state.set_data({
        "user_id": user_id,
        "market_msg": market_msg
    })


@dp.callback_query_handler(regexp=regexps.MarketRegexp.back)
async def back_market_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    market_msg: types.Message = data.get("market_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(text=msg_text)

    if callback.data == "back_market":
        await market_msg.edit_text(
            text=market_msg.html_text,
            reply_markup=market_msg.reply_markup,
        )

    await callback.answer()


@dp.callback_query_handler(regexp=regexps.MarketRegexp.menu)
async def market_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    market_msg: types.Message = data.get("market_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    page_move = re.findall(r"page_(\d+)", callback.data)
    select_product = re.findall(r"market_product_(\d+)", callback.data)

    if page_move:
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id
        )
        page = int(page_move[0])
        keyboard = keyboard.create_market_keyboard(page)
        try:
            msg_text = read_txt_file("text/market/list_products")
            await market_msg.edit_text(
                text=msg_text.format(page+1, keyboard[1]),
                reply_markup=keyboard[0]
            )
        except exceptions.MessageNotModified:
            pass

    elif select_product:
        product_id = int(select_product[0])

        session = db_api.CreateSession()
        product: tables.Market = session.db.query(tables.Market).filter_by(
            id=product_id
        ).first()
        if product is None:
            return await callback.answer("Этот товар уже кто-то купил.")

        user_table: tables.User = session.filter_by_user_id(
            user_id=product.user_id,
            table=tables.User
        )

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id
        )
        keyboard = keyboard.create_product_keyboard(product.user_id)

        time_left = timer.Timer.get_left_time(product.timer)

        msg_text = read_txt_file("text/market/about_product")
        await market_msg.edit_text(
            text=msg_text.format(
                product.count,
                product.product,
                product.price,
                user_table.first_name,
                *time_left
            ),
            reply_markup=keyboard
        )
        await state.update_data({
            "product_id": product_id,
        })
        session.close()

    elif callback.data == "my_products":
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id
        )
        keyboard = keyboard.create_user_products_keyboard()

        msg_text = read_txt_file("text/market/user_products")
        await market_msg.edit_text(
            text=msg_text,
            reply_markup=keyboard
        )

    await callback.answer()


@dp.callback_query_handler(regexp=regexps.MarketRegexp.current_product)
async def market_product_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    market_product_id = data.get("product_id")

    market_msg: types.Message = data.get("market_msg")
    if callback.data == "back_products_list":
        await market_msg.edit_text(
            text=market_msg.html_text,
            reply_markup=market_msg.reply_markup,
        )
        return

    session = db_api.CreateSession()
    sell_product: tables.Market = session.db.query(tables.Market).filter_by(
        id=market_product_id
    ).first()

    seller_townhall_table: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=sell_product.user_id).first()

    buyer_townhall_table: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    seller_manufacture_table: tables.Manufacture = session.db.query(
        tables.Manufacture).filter_by(user_id=sell_product.user_id).first()

    buyer_manufacture_table: tables.Manufacture = session.db.query(
        tables.Manufacture).filter_by(user_id=user_id).first()

    base_products = ages.Age.get_all_products()
    base_products = [i.name for i in base_products]

    if callback.data == "buy_product":
        if sell_product is None:
            await callback.answer("упс, кто-то уже купил")

            keyboard = kb_constructor.PaginationKeyboard(
                user_id=user_id).create_market_keyboard()

            await market_msg.edit_text(
                text=market_msg.html_text,
                reply_markup=keyboard[0],
            )
            return session.close()

        if buyer_townhall_table.money >= sell_product.price:

            buyer_townhall_table.money -= sell_product.price
            seller_townhall_table.money += sell_product.price

            base_sell_product_id = base_products.index(sell_product.product)
            buyer_manufacture_table_storage = list(buyer_manufacture_table.storage)

            buyer_products_id = [
                product["product_id"] for product in buyer_manufacture_table_storage
            ]

            for product in buyer_manufacture_table_storage:
                index = buyer_manufacture_table_storage.index(product)
                product_id = product["product_id"]
                product_count = product["count"]

                if product_id == base_sell_product_id:
                    product_count += sell_product.count
                    buyer_manufacture_table_storage[index] = {
                        "product_id": product_id,
                        "count": product_count
                    }

            if base_sell_product_id not in buyer_products_id:
                buyer_manufacture_table_storage.append(
                    {
                        "product_id": base_sell_product_id,
                        "count": sell_product.count
                    }
                )
            buyer_manufacture_table.storage = buyer_manufacture_table_storage

            session.db.query(tables.Market).filter_by(id=market_product_id).delete()
            session.db.commit()

            keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
            keyboard = keyboard.create_market_keyboard()
            await market_msg.edit_text(
                text=market_msg.html_text,
                reply_markup=keyboard[0],
            )
            await bot.send_message(
                chat_id=seller_townhall_table.user_id,
                text="🌟 Ваш товар <b>x{} {}</b>, купили за {} 💰.".format(
                    sell_product.count, sell_product.product, sell_product.price
                )
            )

        else:
            msg_text = read_txt_file("text/hints/few_money")
            await callback.answer(
                text=msg_text
            )

    elif callback.data == "delete_product":
        if sell_product is None:
            keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
            keyboard = keyboard.create_market_keyboard()
            await market_msg.edit_text(
                text=market_msg.html_text,
                reply_markup=keyboard[0],
            )
            await callback.answer("упс, кто-то уже купил")
            # await states.Market.products_list.set()
            return session.close()

        seller_manufacture_table_storage = list(seller_manufacture_table.storage)
        base_sell_product_id = base_products.index(sell_product.product)

        seller_products_id = [
            product["product_id"] for product in seller_manufacture_table_storage
        ]

        for product in seller_manufacture_table_storage:
            product_id = product["product_id"]
            product_count = product["count"]

            index = seller_manufacture_table_storage.index(product)
            if product_id == base_sell_product_id:
                product_count += sell_product.count
                seller_manufacture_table_storage[index] = {
                    "product_id": product_id,
                    "count": product_count
                }

        if base_sell_product_id not in seller_products_id:
            seller_manufacture_table_storage.append(
                {
                    "product_id": base_sell_product_id,
                    "count": sell_product.count
                }
            )

        seller_manufacture_table.storage = seller_manufacture_table_storage

        session.db.query(tables.Market).filter_by(
            id=market_product_id).delete()
        session.db.commit()

        keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
        keyboard = keyboard.create_market_keyboard()
        await market_msg.edit_text(
            text=market_msg.html_text,
            reply_markup=keyboard[0],
        )

    await callback.answer()
    session.close()

