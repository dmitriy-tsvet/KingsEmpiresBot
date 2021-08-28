from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from utils.misc.read_file import read_txt_file

from utils.classes import kb_constructor, timer
from utils.db_api import db_api, tables
from utils.ages import models
from utils.misc.operation_with_lists import subtract_nums_list, add_nums_list

import states
import re


@dp.message_handler(state="*", commands="market")
async def market_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id
    )
    keyboard = keyboard.create_products_list_keyboard()

    msg_text = read_txt_file("text/market/list_products")
    edit_msg = await message.answer(
        msg_text.format(1, keyboard[1]),
        reply_markup=keyboard[0]
    )

    await state.set_data({
        "edit_msg": edit_msg
    })
    await states.Market.products_list.set()


@dp.callback_query_handler(state=states.Market.products_list)
async def products_list_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = callback.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    page_move = re.findall(r"page_(\d+)", callback.data)
    select_product = re.findall(r"product_(\d+)", callback.data)

    if callback.data == "back_products_list":
        await data["edit_msg"].edit_text(
            text=data["edit_msg"].html_text,
            reply_markup=data["edit_msg"].reply_markup,
        )
        await states.Market.products_list.set()
        return

    if page_move:
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id
        )
        page = int(page_move[0])
        keyboard = keyboard.create_products_list_keyboard(page)
        try:
            msg_text = read_txt_file("text/market/list_products")
            await edit_msg.edit_text(
                text=msg_text.format(page+1, keyboard[1]),
                reply_markup=keyboard[0]
            )
        except exceptions.MessageNotModified:
            pass

    elif select_product:
        product_id = int(select_product[0])

        new_session = db_api.NewSession()
        product: tables.Market = new_session.session.query(tables.Market).filter_by(
            id=product_id
        ).first()
        if product is None:
            return await callback.answer("Этот товар уже кто-то купил.")

        user_table: tables.User = new_session.filter_by_user_id(
            user_id=product.user_id,
            table=tables.User
        )

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id
        )
        keyboard = keyboard.create_product_keyboard(product.user_id)

        time_left = timer.Timer.get_left_time(product.timer)

        msg_text = read_txt_file("text/market/about_product")
        await edit_msg.edit_text(
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
        await states.Market.current_product.set()

    elif callback.data == "my_products":
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id
        )
        keyboard = keyboard.create_user_products_keyboard()

        msg_text = read_txt_file("text/market/user_products")
        await edit_msg.edit_text(
            text=msg_text,
            reply_markup=keyboard
        )

    await callback.answer()


@dp.callback_query_handler(state=states.Market.current_product)
async def products_list_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    product_id = data.get("product_id")

    if callback.data == "back_products_list":
        await data["edit_msg"].edit_text(
            text=data["edit_msg"].html_text,
            reply_markup=data["edit_msg"].reply_markup,
        )
        await states.Market.products_list.set()
        return
    new_session = db_api.NewSession()
    product: tables.Market = new_session.session.query(tables.Market).filter_by(
        id=product_id
    ).first()

    buyer_townhall_table: tables.TownHall = new_session.filter_by_user_id(
        user_id=user_id,
        table=tables.TownHall
    )

    seller_townhall_table: tables.TownHall = new_session.filter_by_user_id(
        user_id=product.user_id,
        table=tables.TownHall
    )

    seller_units_table: tables.Units = new_session.filter_by_user_id(
        user_id=product.user_id,
        table=tables.Units
    )

    buyer_units_table: tables.Units = new_session.filter_by_user_id(
        user_id=user_id,
        table=tables.Units
    )


    if callback.data == "buy_product":
        if product is None:
            await callback.answer("упс, кто-то уже купил")

            keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
            keyboard = keyboard.create_products_list_keyboard()
            await data["edit_msg"].edit_text(
                text=data["edit_msg"].html_text,
                reply_markup=keyboard[0],
            )

            return new_session.close()

        if buyer_townhall_table.money >= product.price:

            buyer_townhall_table.money -= product.price
            seller_townhall_table.money += product.price

            if product.product == "🍇":
                buyer_townhall_table.food += product.count
            elif product.product == "🌲":
                buyer_townhall_table.stock += product.count
            elif product.product == "💂":
                buyer_units_table.all_unit_counts += product.count

                units_count = list(buyer_units_table.unit_counts)
                buyer_units_table.unit_counts = add_nums_list(
                    product.count, units_count
                )

            new_session.session.query(tables.Market).filter_by(id=product_id).delete()
            new_session.session.commit()

            keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
            keyboard = keyboard.create_products_list_keyboard()
            await data["edit_msg"].edit_text(
                text=data["edit_msg"].html_text,
                reply_markup=keyboard[0],
            )
            await callback.answer("-{} 💰".format(product.price))
            await states.Market.products_list.set()

        else:
            msg_text = read_txt_file("text/hints/few_money")
            await callback.answer(
                text=msg_text
            )

    elif callback.data == "delete_product":
        if product is None:
            keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
            keyboard = keyboard.create_products_list_keyboard()
            await data["edit_msg"].edit_text(
                text=data["edit_msg"].html_text,
                reply_markup=keyboard[0],
            )
            await callback.answer("упс, кто-то уже купил")
            await states.Market.products_list.set()
            return new_session.close()

        if product.product == "🍇":
            seller_townhall_table.food += product.count
        elif product.product == "🌲":
            seller_townhall_table.stock += product.count
        elif product.product == "units":
            seller_townhall_table.all_unit_counts += product.count

            units_count = list(seller_townhall_table.unit_counts)
            seller_townhall_table.unit_counts = add_nums_list(
                product.count, units_count
            )
        
        # delete all
        new_session.session.query(tables.Market).filter_by(
            id=product_id).delete()
        new_session.session.commit()

        keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
        keyboard = keyboard.create_products_list_keyboard()
        await data["edit_msg"].edit_text(
            text=data["edit_msg"].html_text,
            reply_markup=keyboard[0],
        )
        await callback.answer("-{} 💰".format(product.price))
        await states.Market.products_list.set()

    new_session.close()

