import states
from loader import dp
from data import config

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from utils.misc.read_file import read_txt_file

from utils.db_api import db_api, tables

from utils.classes import transaction, kb_constructor, timer, table_setter, hour_income
from utils.models import ages

from utils.models import models, base
from utils.misc.regexps import TownhallRegexp

import re
import typing
import keyboards


@dp.message_handler(state="*", commands="townhall")
async def townhall_command_handler(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    user_id = message.from_user.id
    user_mention = message.from_user.get_mention()

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()
    progress: tables.Progress = session.db.query(
        tables.Progress).filter_by(user_id=user_id).first()
    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()
    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

    session.db.commit()

    if clan_member is None:
        msg_text = read_txt_file("text/townhall/townhall_none_clan")
        user_clan = ""
    else:
        msg_text = read_txt_file("text/townhall/townhall_in_clan")
        user_clan = "{}".format(
            clan_member.clan.name,
        )

    base_age: models.Age = ages.Age.get(townhall.age)
    progress_score = hour_income.HourIncome(user_id=user_id).get_progress_score_income()
    if progress.score < 10:
        progress.score += progress_score

    keyboard = kb_constructor.StandardKeyboard(
        user_id=user_id).create_townhall_keyboard()

    with open(base_age.townhall_img, 'rb') as sticker:
        await message.answer_sticker(sticker=sticker)

    edit_msg = await message.answer(
        text=msg_text.format(
            townhall.country_name,
            townhall.age,
            townhall.population,
            user_clan,
            user_mention),
        reply_markup=keyboard
    )

    await state.update_data({
        "user_id": user_id,
        "townhall_msg": edit_msg,
        "index": 0
    })
    session.close()


@dp.callback_query_handler(regexp=TownhallRegexp.back)
async def townhall_back_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(text=msg_text)

    townhall_msg: types.Message = data.get("townhall_msg")

    if callback.data == "back_townhall":
        await townhall_msg.edit_text(
            text=townhall_msg.html_text,
            reply_markup=townhall_msg.reply_markup,
        )
        return


@dp.callback_query_handler(regexp=TownhallRegexp.menu)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(text=msg_text)

    townhall_msg: types.Message = data.get("townhall_msg")

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()
    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()
    progress: tables.Progress = session.db.query(
        tables.Progress).filter_by(user_id=user_id).first()

    if callback.data == "progress":
        all_ages = ages.Age.get_all_ages()
        age_index = all_ages.index(townhall.age)
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_progress_keyboard(age_index)

        msg_text = read_txt_file("text/townhall/progress")
        await townhall_msg.edit_text(
            text=msg_text.format(
                progress.score),
            reply_markup=keyboard
        )

    elif callback.data == "storage":
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_storage_keyboard()

        msg_text = read_txt_file("text/townhall/storage")
        await townhall_msg.edit_text(
            text=msg_text.format(
                townhall.stock,
                townhall.money,
                townhall.diamonds
            ),
            reply_markup=keyboard
        )

    income = hour_income.HourIncome(user_id=user_id)

    if callback.data == "get_money":
        current_income = income.get_money_income()
        townhall.money += current_income
        townhall.timer = timer.Timer.set_timer(3600)
        await callback.answer("+ {} 💰".format(current_income), show_alert=False)

    elif callback.data == "get_stock":
        current_income = income.get_stock_income()
        townhall.stock += current_income
        buildings.timer = timer.Timer.set_timer(3600)
        await callback.answer("+ {} ⚒".format(current_income), show_alert=False)

    session.close()


@dp.callback_query_handler(regexp=TownhallRegexp.storage)
async def progress_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(text=msg_text)

    townhall_msg: types.Message = data.get("townhall_msg")

    session = db_api.CreateSession()
    all_products = ages.Age.get_all_products()

    manufacture: tables.Manufacture = session.db.query(
        tables.Manufacture).filter_by(user_id=user_id).first()
    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    my_product = re.findall(r"my_product_(\d+)", callback.data)
    if my_product:
        product_id = int(my_product[0])
        base_product = all_products[product_id]

        stock_income = 0

        storage = list(manufacture.storage)
        for product in manufacture.storage:
            if product["product_id"] == product_id:
                new_product = {
                    "product_id": product_id,
                    "count": product["count"]-1
                }
                stock_income = base_product.income
                townhall.stock += stock_income

                if new_product["count"] <= 0:
                    storage.remove(product)
                else:
                    index = storage.index(product)
                    storage.remove(product)
                    storage.insert(index, new_product)

        manufacture.storage = storage
        session.db.commit()
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_storage_keyboard()
        msg_text = read_txt_file("text/townhall/storage")
        await townhall_msg.edit_text(
            text=msg_text.format(
                townhall.stock,
                townhall.money,
                townhall.diamonds
            ),
            reply_markup=keyboard
        )

        await callback.answer("+{} ⚒".format(stock_income))

    session.close()


@dp.callback_query_handler(regexp=TownhallRegexp.progress)
async def progress_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(text=msg_text)

    townhall_msg: types.Message = data.get("townhall_msg")

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()
    progress: tables.Progress = session.db.query(
        tables.Progress).filter_by(user_id=user_id).first()
    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    base_age: base.Age = ages.Age.get(townhall.age)
    progress_tree = ages.Age.get_all_trees()

    get_technology = re.findall(r"technology_(\d+)_(\d+)", callback.data)

    page_move = re.findall(r"tree_page_(\d+)", callback.data)

    if page_move:
        page = int(page_move[0])
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_progress_keyboard(page)

        try:
            await townhall_msg.edit_reply_markup(
                reply_markup=keyboard
            )
        except exceptions.MessageNotModified:
            pass

    if get_technology:
        branch_index = int(get_technology[0][0])
        technology_index = int(get_technology[0][1])

        technology: base.Technology = ages.Age.get_all_trees()[branch_index][technology_index]

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_technology_keyboard(
            branch_index=branch_index, technology_index=technology_index)

        msg_text = read_txt_file("text/townhall/technology")
        unlock_price = transaction.Purchase.get_price(technology.unlock_price)
        await townhall_msg.edit_text(
            text=msg_text.format(
                technology.name,
                str(technology.unlock_technology),
                progress.tree[branch_index][technology_index],
                technology.unlock_score,
                unlock_price
            ),
            reply_markup=keyboard
        )
        await state.update_data({
            "branch_index": branch_index,
            "technology_index": technology_index
        })

    elif callback.data == "upgrade_one":
        branch_index = data.get("branch_index")
        technology_index = data.get("technology_index")

        if (branch_index is None) or (technology_index is None):
            await callback.answer()
            session.close()
            return

        if progress.score < 1:
            await callback.answer(
                text="Вам не хватает 🧬 Очков Науки."
            )
            session.close()
            return

        technology: base.Technology = progress_tree[branch_index][technology_index]

        tree = list(progress.tree)
        branch = list(tree[branch_index])

        if branch[technology_index] >= technology.unlock_score:
            await callback.answer(
                text="Эта технология уже открыта."
            )
            session.close()
            return

        previous_branch_index = branch_index-1

        user_previous_branch = []
        base_previous_branch = []
        if previous_branch_index >= 0:

            for i in tree[previous_branch_index]:
                if i is not None:
                    i -= 1
                user_previous_branch.append(i)

            for tech in progress_tree[previous_branch_index]:
                if type(tech) is base.Technology:
                    tech = tech.unlock_score
                base_previous_branch.append(tech)

        coincidences = []

        if base_previous_branch.count(None) == 2:
            if base_previous_branch == user_previous_branch:
                coincidences.append(None)
        else:
            if branch.count(None) == 2:
                for i in base_previous_branch:
                    index = base_previous_branch.index(i)
                    if i is None:
                        continue
                    elif i == user_previous_branch[index]:
                        coincidences.append(None)
            else:
                if user_previous_branch[technology_index] == base_previous_branch[technology_index]:
                    coincidences.append(None)

        if not coincidences and base_previous_branch:
            await callback.answer(
                text="У вас не открыта предыдущая ветка."
            )
            session.close()
            return

        branch[technology_index] += 1
        tree[branch_index] = branch
        progress.tree = tree
        progress.score -= 1
        session.db.commit()

        technology: base.Technology = progress_tree[branch_index][technology_index]

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_technology_keyboard(
            branch_index=branch_index, technology_index=technology_index)

        msg_text = read_txt_file("text/townhall/technology")
        unlock_price = transaction.Purchase.get_price(technology.unlock_price)
        await townhall_msg.edit_text(
            text=msg_text.format(
                technology.name,
                str(technology.unlock_technology),
                progress.tree[branch_index][technology_index],
                technology.unlock_score,
                unlock_price
            ),
            reply_markup=keyboard
         )

    # unlock all
    elif callback.data == "upgrade_all":
        branch_index = data.get("branch_index")
        technology_index = data.get("technology_index")

        if (branch_index is None) or (technology_index is None):
            await callback.answer()
            session.close()
            return

        if progress.score < 1:
            await callback.answer(
                text="Вам не хватает очков 🧬 Науки."
            )
            session.close()
            return

        tree = list(progress.tree)
        branch = list(tree[branch_index])

        technology: base.Technology = progress_tree[branch_index][technology_index]

        if branch[technology_index] >= technology.unlock_score:
            await callback.answer(
                text="Эта технология уже открыта."
            )
            session.close()
            return

        previous_branch_index = branch_index - 1

        user_previous_branch = []
        base_previous_branch = []
        if previous_branch_index >= 0:

            for i in tree[previous_branch_index]:
                if i is not None:
                    i -= 1
                user_previous_branch.append(i)

            for tech in progress_tree[previous_branch_index]:
                if type(tech) is base.Technology:
                    tech = tech.unlock_score
                base_previous_branch.append(tech)

        coincidences = []

        if base_previous_branch.count(None) == 2:
            if base_previous_branch == user_previous_branch:
                coincidences.append(None)
        else:
            if branch.count(None) == 2:
                for i in base_previous_branch:
                    index = base_previous_branch.index(i)
                    if i is None:
                        continue
                    elif i == user_previous_branch[index]:
                        coincidences.append(None)
            else:
                print(technology_index, user_previous_branch, base_previous_branch)
                if user_previous_branch[technology_index] == base_previous_branch[technology_index]:
                    coincidences.append(None)

        if not coincidences and base_previous_branch:
            await callback.answer(
                text="У вас не открыта предыдущая ветка."
            )
            session.close()
            return

        unlock_score = technology.unlock_score
        unlock_score -= progress.score

        for i in range(0, progress.score):
            if branch[technology_index] == technology.unlock_score:
                break
            branch[technology_index] += 1
            progress.score -= 1

        tree[branch_index] = branch
        progress.tree = tree

        msg_text = read_txt_file("text/townhall/progress")

        session.db.commit()

        all_ages = ages.Age.get_all_ages()
        age_index = all_ages.index(townhall.age)
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_progress_keyboard(age_index)

        await townhall_msg.edit_text(
            text=msg_text.format(progress.score),
            reply_markup=keyboard
        )

    elif callback.data == "unlock_tech":
        branch_index = data.get("branch_index")
        technology_index = data.get("technology_index")

        if (branch_index is None) or (technology_index is None):
            await callback.answer()
            session.close()
            return

        base_buildings: typing.List[typing.Union[
            base.BuilderHome, base.StockBuilding, base.ClanBuilding,
            base.ManufactureBuilding
        ]] = ages.Age.get_all_buildings()
        base_units: typing.List[base.Unit] = ages.Age.get_all_units()
        technology: base.Technology = progress_tree[branch_index][technology_index]
        tree = list(progress.tree)
        branch = list(tree[branch_index])

        if branch[technology_index] > technology.unlock_score:
            await callback.answer(
                text="Эта технология уже открыта."
            )
            session.close()
            return

        buying = transaction.Purchase.buy(
            price=technology.unlock_price,
            townhall=townhall
        )

        if not buying:
            price = transaction.Purchase.get_dynamic_price(
                price=technology.unlock_price,
                townhall=townhall
            )
            msg_text = read_txt_file("text/hints/few_money")
            await callback.answer(
                text=msg_text.format(price)
            )
            session.close()
            return

        if type(technology.unlock_technology) in (
                base.StockBuilding, base.ManufactureBuilding, base.HomeBuilding):
            unlocked_buildings = list(progress.unlocked_buildings)
            unlocked_buildings.append(base_buildings.index(technology.unlock_technology))
            progress.unlocked_buildings = unlocked_buildings

        elif type(technology.unlock_technology) is base.Unit:
            unlocked_units = list(units.units_type)

            unlocked_units[
                base_age.units.index(technology.unlock_technology)] = base_units.index(
                technology.unlock_technology)

            units.units_type = unlocked_units

        branch[technology_index] += 1
        tree[branch_index] = branch
        progress.tree = tree
        session.db.commit()

        all_ages = ages.Age.get_all_ages()
        age_index = all_ages.index(townhall.age)
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_progress_keyboard(age_index)

        msg_text = read_txt_file("text/townhall/progress")
        await townhall_msg.edit_text(
            text=msg_text.format(progress.score),
            reply_markup=keyboard
        )

    elif callback.data == "unlock_age":
        branch_index = len(progress.tree)
        previous_branch_index = branch_index-1

        user_previous_branch = []
        base_previous_branch = []

        if previous_branch_index >= 0:
            for i in progress.tree[previous_branch_index]:
                if i is not None:
                    i -= 1
                user_previous_branch.append(i)

            for tech in progress_tree[previous_branch_index]:
                if type(tech) is base.Technology:
                    tech = tech.unlock_score
                base_previous_branch.append(tech)

        coincidences = []

        for i in user_previous_branch:
            index = user_previous_branch.index(i)
            if i is None:
                continue
            elif i == base_previous_branch[index]:
                coincidences.append(None)

        if not coincidences:
            await callback.answer(
                text="У вас не открыта предыдущая ветка."
            )
            session.close()
            return

        await callback.message.answer("🌟")
        msg_text = read_txt_file("text/townhall/next_age")
        list_ages = ages.Age.get_all_ages()
        next_age_name = list_ages[list_ages.index(townhall.age)+1]
        townhall.age = next_age_name
        base_age = ages.Age.get(townhall.age)

        session.db.commit()

        techs = ""
        new_tree = []

        progress_tree = ages.Age.get(next_age_name).progress_tree

        for branch in progress_tree:
            new_branch = []
            for tech in branch:
                if tech is not None:
                    techs += "- <i>{}</i>\n".format(tech.name)
                    new_branch.append(0)
                else:
                    new_branch.append(tech)
            new_tree.append(new_branch)

        new_tree = progress.tree + new_tree
        progress.tree = new_tree
        await callback.message.reply(msg_text.format(
            townhall.country_name, callback.from_user.get_mention(),
            next_age_name,
            techs
        ))

    await callback.answer()
    session.close()





