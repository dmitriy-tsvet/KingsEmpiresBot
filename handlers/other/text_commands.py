from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
import re
import typing
from utils.misc.read_file import read_txt_file
from utils.classes import timer, transaction

from utils.ages import models, ages_list
from utils.db_api import tables, db_api
from utils.misc.operation_with_lists import subtract_nums_list, add_nums_list

forwarding_units = r"отправить (\d+) (воинов|воина)"
sell_product = r"продать (\d+) (провизия|сырье|юнит) за (\d+)"
price = r"цена|прайс"


@dp.message_handler(filters.IsReplyFilter(True), regexp=forwarding_units, state="*")
async def forwarding_units_handler(message: types.Message, state: FSMContext):
    replied_user_id = message.reply_to_message.from_user.id
    user_id = message.from_user.id

    replied_mention = message.reply_to_message.from_user.get_mention()
    mention = message.from_user.get_mention()

    is_bot = message.reply_to_message.from_user.is_bot
    if replied_user_id != user_id and not is_bot:

        count_forward_units = int(re.findall(r"(\d+)", message.text)[0])

        if count_forward_units < 1:
            return message.reply(
                "😿 А почему так мало?"
            )

        new_session = db_api.NewSession()

        units_table: tables.Units = new_session.filter_by_user_id(
            user_id=user_id, table=tables.Units)
        replied_units_table: tables.Units = new_session.filter_by_user_id(
            user_id=replied_user_id, table=tables.Units)

        if count_forward_units > units_table.all_unit_counts:
            await message.reply("У тебя нету такого количества воинов.")
        else:
            units_table.all_unit_counts -= count_forward_units
            units_count_1 = list(units_table.unit_counts)
            units_table.unit_counts = subtract_nums_list(
                count_forward_units, units_count_1
            )

            replied_units_table.all_unit_counts += count_forward_units
            units_count_2 = list(replied_units_table.unit_counts)

            replied_units_table.unit_counts = add_nums_list(
                count_forward_units, units_count_2
            )

            sticker = read_txt_file("sticker/forward_units")

            await message.answer_sticker(sticker=sticker)
            await message.answer(
                "<i>{} высылает боевую поддержку {},\n"
                "в размере 💂 {} воинов.</i>".format(
                    mention, replied_mention, count_forward_units
                ))

        new_session.close()


@dp.message_handler(regexp=sell_product, state="*")
async def sell_product(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    result = re.findall(
        r"[П, п]родать (\d+) (провизия|сырье|юнит) за (\d+)", message.text)[0]

    to_emoji = {
        "провизия": "🍇",
        "сырье": "🌲",
        "юнит": "💂"
    }

    product_name = to_emoji[result[1]]
    count = int(result[0])
    price = int(result[2])

    new_session = db_api.NewSession()
    townhall_table: tables.TownHall = new_session.filter_by_user_id(
            user_id=user_id, table=tables.TownHall
        )
    units_table: tables.Units = new_session.filter_by_user_id(
            user_id=user_id, table=tables.Units
        )

    market_table: typing.List[tables.Market] = new_session.session.query(
        tables.Market).filter_by(user_id=user_id).all()
    if len(market_table) == 8:
        await message.reply(
            text="<b>У тебя достигнут лимит.</b>\n\n"
                 "<i>Удали какой-нибудь товар\n"
                 "прежде, чем добавить новый.</i>"
        )
        return new_session.close()

    if product_name == "🍇":
        if townhall_table.food >= count:
            townhall_table.food -= count
        else:
            await message.reply("<i>У тебя только x{} {}.</i>".format(
                townhall_table.food, product_name))
            return new_session.close()
    elif product_name == "🌲":
        if townhall_table.stock >= count:
            townhall_table.stock -= count
        else:
            await message.reply("<i>У тебя только x{} {}.</i>".format(
                townhall_table.stock, product_name))
            return new_session.close()
    elif product_name == "💂":
        if units_table.all_unit_counts >= count:
            units_table.all_unit_counts -= count

            units_count = list(units_table.unit_counts)
            units_table.unit_counts = subtract_nums_list(
                count, units_count
            )

        else:
            await message.reply("<i>У тебя только x{} {}.</i>".format(
                units_table.all_unit_counts, product_name))
            return new_session.close()

    time_set = timer.Timer.set_timer(86400)

    product = tables.Market(
        user_id=user_id,
        product=product_name,
        price=price,
        count=count,
        timer=time_set
    )
    new_session.session.add(product)
    await message.reply(
        text="Товар успешно добавлен."
    )
    new_session.close()


@dp.message_handler(filters.IsReplyFilter(True), regexp=price, state="*")
async def sell_product(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_session = db_api.NewSession()
    townhall_table: tables.TownHall = new_session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall
    )
    current_state = await state.get_state()
    age_model: models.Age = ages_list.AgesList.get_age_model(townhall_table.age)

    if current_state == "Units:menu":
        text = ""
        for unit in age_model.units:
            create_price = transaction.Transaction.get_text_price(
                unit.create_price)

            text += "x1{} - {}\n".format(unit.name, create_price)

        await message.reply(
            text=text
        )

    elif current_state == "Citizens:menu":

        create_price = transaction.Transaction.get_text_price(
            age_model.citizen.create_price)

        text = "x1{} Житель - {}\n".format(
            age_model.citizen.name,
            create_price)

        await message.reply(
            text=text
        )
