from loader import dp
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
import re
import typing
from utils.classes import timer, kb_constructor, regexps

from utils.models import ages, clan_building, base
from utils.db_api import tables, db_api
from utils.misc.operation_with_lists import subtract_nums_list, add_nums_list

sell_product = r"продать\s+(\d+)\s+(.*)\s+за\s+(\d+)"
price = r"цена|прайс"


@dp.message_handler(filters.IsReplyFilter(True), regexp=regexps.ClanRegexp.donate, state="*")
async def forwarding_units_handler(message: types.Message, state: FSMContext):
    replied_user_id = message.reply_to_message.from_user.id
    user_id = message.from_user.id

    mention = message.from_user.get_mention()

    is_bot = message.reply_to_message.from_user.is_bot
    if replied_user_id != user_id and is_bot:

        session = db_api.CreateSession()

        country_name = re.findall(r"(.+)\s+\( 🤴", message.reply_to_message.text)

        if not country_name:
            return

        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=user_id).first()

        townhall_replied: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(country_name=country_name[0]).first()

        clan_member: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(user_id=townhall_replied.user_id).first()

        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=townhall_replied.user_id).first()

        units_table: tables.Units = session.db.query(
            tables.Units).filter_by(user_id=user_id).first()

        replied_units_table: tables.Units = session.db.query(
            tables.Units).filter_by(user_id=townhall_replied.user_id).first()

        if country_name[0] == townhall.country_name:
            return

        count_forward_units = int(re.findall(r"(\d+)", message.text)[0])

        if count_forward_units < 1:
            session.close()
            return await message.reply(
                text="Слишком мало."
            )
        max_clan_units = buildings.clan_building_lvl * clan_building.clan_building.capacity

        if count_forward_units > sum(units_table.units_count):
            await message.reply("У тебя нету столько.")
        elif clan_member.clan_units == max_clan_units:
            await message.reply("Клановая Крепость уже полна.")
        else:

            base_units = ages.Age.get_all_units()
            clan_member.clan_units += count_forward_units

            remainder_units = 0
            if clan_member.clan_units > max_clan_units:
                remainder_units = clan_member.clan_units - max_clan_units
                clan_member.clan_units = max_clan_units

            array_with_nums = [0 for i in range(0, 5)]
            units_table_copy = add_nums_list(
                count_forward_units - remainder_units, array_with_nums
            )
            real_units_count = 0
            for unit_type in units_table.units_type:
                if type(unit_type) is int:
                    index = units_table.units_type.index(unit_type)
                    if units_table_copy[index] != 0:
                        real_units_count += base_units[unit_type].weight * units_table_copy[index]

            if real_units_count == 0:
                await message.reply("У тебя нету столько.")
                session.close()
                return

            replied_units = [i for i in replied_units_table.units_count if i != 0]

            replied_units = add_nums_list(
                count_forward_units-remainder_units, replied_units
            )
            replied_units += [0, 0, 0, 0, 0]
            replied_units_table.units_count = replied_units[:5]

            units_count_sender = list(units_table.units_count)
            units_table.units_count = subtract_nums_list(
                count_forward_units-remainder_units, units_count_sender
            )
            replied_units_table.real_units_count += real_units_count
            units_table.real_units_count -= real_units_count

            session.db.commit()

            await message.answer(
                "<i>{} высылает боевую поддержку\n"
                "в размере 💂 {} воинов.</i>".format(
                    mention, count_forward_units-remainder_units
                ))

            keyboard = kb_constructor.StandardKeyboard(
                user_id=townhall_replied.user_id).create_get_clan_units_keyboard()
            await message.reply_to_message.edit_reply_markup(keyboard)

        session.close()


@dp.message_handler(regexp=sell_product, state="*")
async def sell_product(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    all_products = []

    session = db_api.CreateSession()

    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()
    manufacture: tables.Manufacture = session.db.query(
            tables.Manufacture).filter_by(user_id=user_id).first()

    base_buildings = ages.Age.get_all_buildings()
    curnt_buildings = [base_buildings[i] for i in buildings.buildings if type(i) is int]

    for building in curnt_buildings:
        if type(building) is base.ManufactureBuilding:
            all_products += building.products

    if not all_products:
        await message.reply("Для начала вам нужна Мануфактура.")
        session.close()
        return

    unlocked_products = [product.name for product in all_products]

    result = re.findall(
        r"продать\s+(\d+)\s+(.*)\s+за\s+(\d+)", message.text)[0]

    product_name = result[1]
    print(product_name)
    count = int(result[0])
    price = int(result[2])

    reg = re.compile(r"\W+\s+(?i)({})".format(product_name))
    selling_product = list(filter(reg.match, unlocked_products))
    print(selling_product)
    if not selling_product:
        await message.reply("Нету такого товара.")
        session.close()
        return

    elif count < 1:
        await message.reply("Слишком мало.")
        session.close()
        return

    manufacture_storage = list(manufacture.storage)
    products_id = [product["product_id"] for product in manufacture_storage]
    print(products_id)
    if unlocked_products.index(selling_product[0]) not in products_id:
        await message.reply("У вас нету этого товара.")
        session.close()
        return
    manufacture_storage_copy = manufacture_storage[:]
    for product in manufacture_storage_copy:
        index = manufacture_storage_copy.index(product)
        product_id = product["product_id"]
        product_count = product["count"]

        products_id.append(product["product_id"])
        if product_id == unlocked_products.index(selling_product[0]):
            if count > product_count:
                await message.reply("У тебя только <b>x{} {}.</b>".format(
                    product_count,
                    selling_product[0])
                )
                session.close()
                return
            else:
                product_count -= count
                if product_count < 1:
                    manufacture_storage.remove(product)
                else:
                    manufacture_storage[index] = {
                        "product_id": product_id,
                        "count": product_count
                    }

    market_table: typing.List[tables.Market] = session.db.query(
        tables.Market).filter_by(user_id=user_id).all()
    if len(market_table) == 8:
        await message.reply(
            text="<b>У тебя достигнут лимит.</b>\n\n"
                 "<i>Удали какой-нибудь товар\n"
                 "прежде, чем добавить новый.</i>"
        )
        return session.close()

    time_set = timer.Timer.set_timer(86400)

    product = tables.Market(
        user_id=user_id,
        product=selling_product[0],
        price=price,
        count=count,
        timer=time_set
    )

    manufacture.storage = manufacture_storage
    session.db.add(product)
    session.db.commit()
    await message.reply(
        text="Товар успешно добавлен."
    )

    session.close()


# @dp.message_handler(filters.IsReplyFilter(True), regexp=price, state="*")
# async def sell_product(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     new_session = db_api.CreateSession()
#     townhall_table: tables.TownHall = new_session.filter_by_user_id(
#         user_id=user_id, table=tables.TownHall
#     )
#     current_state = await state.get_state()
#     age_model: models.Age = ages.AgesList.get_age_model(townhall_table.age)
#
#     if current_state == "Units:menu":
#         text = ""
#         for unit in age_model.units:
#             create_price = transaction.Transaction.get_text_price(
#                 unit.create_price)
#
#             text += "x1{} - {}\n".format(unit.name, create_price)
#
#         await message.reply(
#             text=text
#         )
#
#     elif current_state == "Citizens:menu":
#
#         create_price = transaction.Transaction.get_text_price(
#             age_model.citizen.create_price)
#
#         text = "x1{} Житель - {}\n".format(
#             age_model.citizen.name,
#             create_price)
#
#         await message.reply(
#             text=text
#         )


