import keyboards
from utils.models import ages, base
from aiogram import types
from utils.db_api import db_api, tables
from utils.models import models, clan_building
from utils.classes import timer, hour_income, transaction
import copy
import re
import json
from sqlalchemy import desc, asc, or_, and_
import typing
import random

buildings_lvl_str = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth"
}


class BaseKeyboard:
    def __init__(self, user_id: int):
        self.user_id = user_id

        self.rows = [[] for i in range(0, 8)]

        self.keyboard = types.InlineKeyboardMarkup()
        self.btn = types.InlineKeyboardButton(
            text="None",
            callback_data="None"
        )

        self.left_btn_mv = copy.deepcopy(self.btn)
        self.left_btn_mv.text = "⊲"

        self.right_btn_mv = copy.deepcopy(self.btn)
        self.right_btn_mv.text = "⊳"


class StandardKeyboard(BaseKeyboard):
    def create_townhall_keyboard(self):

        keyboard = copy.deepcopy(self.keyboard)
        incomer = hour_income.HourIncome(user_id=self.user_id)

        btn_get_tax = types.InlineKeyboardButton(
            text="+ 💰", callback_data="get_money"
        )
        btn_get_stock = types.InlineKeyboardButton(
            text="+ ⚒", callback_data="get_stock"
        )
        keyboard.row(btn_get_tax, btn_get_stock)
        keyboard.add(keyboards.townhall.btn_storage)
        keyboard.add(keyboards.townhall.btn_progress)

        return keyboard

    def create_units_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 3

        session = db_api.CreateSession()

        units: tables.Units = session.db.query(
            tables.Units).filter_by(user_id=self.user_id).first()

        base_units = ages.Age.get_all_units()
        for unit_num in units.units_type:
            btn = copy.deepcopy(self.btn)

            if unit_num is None:
                btn.text = "🔒"
            else:
                unit = base_units[unit_num]
                unit_emoji = re.findall(r"(\W+)", unit.name)[0]
                unit_count = units.units_count[units.units_type.index(unit_num)]
                btn.text = "x{} {}".format(unit_count, unit_emoji)
                btn.callback_data = "unit_{}".format(unit_num)

            keyboard.insert(btn)

        session.close()
        return keyboard

    def create_clan_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 2

        session = db_api.CreateSession()

        clan_member: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(user_id=self.user_id).first()
        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()

        if clan_member.rank in ("Лидер", "Заместитель"):
            keyboard.add(keyboards.clan.btn_war)

        if clan_member.clan_units == \
                buildings.clan_building_lvl*clan_building.clan_building.capacity:
            btn_get_units = types.InlineKeyboardButton(
                text="💂 {} / {}".format(clan_member.clan_units, clan_member.clan_units),
                callback_data="None"
            )
        elif clan_member.clan_units > 0:
            btn_get_units = types.InlineKeyboardButton(
                text="💂 {} / {}".format(
                    clan_member.clan_units,
                    buildings.clan_building_lvl*clan_building.clan_building.capacity
                ),
                callback_data="get_clan_units"
            )
        else:
            btn_get_units = types.InlineKeyboardButton(
                text="🏹 Запросить Воинов", callback_data="get_clan_units"
            )

        keyboard.add(btn_get_units)
        keyboard.row(keyboards.clan.btn_members)

        session.close()
        return keyboard

    def create_get_clan_units_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 2

        session = db_api.CreateSession()

        clan_member: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(user_id=self.user_id).first()
        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()

        btn_get_units = types.InlineKeyboardButton(
            text="💂 {} / {}".format(
                clan_member.clan_units,
                buildings.clan_building_lvl*clan_building.clan_building.capacity
            ),
            callback_data="None"
        )

        keyboard.add(btn_get_units)

        session.close()
        return keyboard

    def create_select_units_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 3

        session = db_api.CreateSession()

        units: tables.Units = session.db.query(
            tables.Units).filter_by(user_id=self.user_id).first()

        base_units = ages.Age.get_all_units()
        for unit_num in units.units_type:
            btn = copy.deepcopy(self.btn)

            if unit_num is None:
                continue
            else:
                unit = base_units[unit_num]
                unit_count = units.units_count[units.units_type.index(unit_num)]
                unit_emoji = re.findall(r"(\W+)", unit.name)[0]
                btn.text = "{} {}".format(unit_count, unit_emoji)
                btn.callback_data = "unit_{}".format(unit_num)

            keyboard.insert(btn)

        session.close()
        return keyboard

    def create_product_keyboard(self, table_user_id: int):
        keyboard = copy.deepcopy(self.keyboard)

        if self.user_id == table_user_id:
            keyboard.add(keyboards.market.btn_delete_product)
        else:
            keyboard.add(keyboards.market.btn_buy_product)

        keyboard.add(keyboards.market.btn_back_market)
        return keyboard

    def create_manufacture_products_keyboard(self, manufacture_building: base.ManufactureBuilding):
        keyboard = copy.deepcopy(self.keyboard)
        products: typing.List[base.ManufactureProduct] = manufacture_building.products
        all_products = ages.Age.get_all_products()
        for product in products:
            btn = copy.deepcopy(self.btn)
            product_emoji = re.findall(r"(\W+)\s+", product.name)[0]
            btn.text = "{}".format(product_emoji)
            btn.callback_data = "create_product_{}".format(all_products.index(product))
            keyboard.insert(btn)
        keyboard.add(keyboards.manufacture.btn_back)

        return keyboard

    def create_storage_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 3

        session = db_api.CreateSession()
        manufacture: tables.Manufacture = session.db.query(
            tables.Manufacture).filter_by(user_id=self.user_id).first()
        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=self.user_id).first()

        all_products = ages.Age.get_all_products()
        for product in manufacture.storage:
            btn = copy.deepcopy(self.btn)
            base_product: base.ManufactureProduct = all_products[product["product_id"]]
            product_emoji = re.findall(r"(\W+)\s+", base_product.name)[0]
            btn.text = "{} {}".format(product["count"], product_emoji)
            btn.callback_data = "my_product_{}".format(product["product_id"])
            keyboard.insert(btn)

        keyboard.add(keyboards.townhall.btn_back_townhall)
        session.close()
        return keyboard

    def create_invitation_keyboard(self, invitation_id: int):
        keyboard = copy.deepcopy(self.keyboard)

        btn_accept_invitation = copy.deepcopy(self.btn)
        btn_cancel_invitation = copy.deepcopy(self.btn)

        btn_accept_invitation.text = "принять"
        btn_accept_invitation.callback_data = "accept_invitation_{}".format(
            invitation_id)

        btn_cancel_invitation.text = "отклонить"
        btn_cancel_invitation.callback_data = "cancel_invitation_{}".format(
            invitation_id)

        keyboard.row(btn_accept_invitation, btn_cancel_invitation)
        keyboard.add(keyboards.clan.btn_back_invitation)
        return keyboard

    def create_member_keyboard(self, member_id: int, member: tables.ClanMember):
        keyboard = copy.deepcopy(self.keyboard)

        if member.rank in ("Лидер", "Заместитель") and member_id != member.id:
            btn_raise_member = copy.deepcopy(self.btn)
            btn_kick_member = copy.deepcopy(self.btn)

            btn_raise_member.text = "повысить"
            btn_raise_member.callback_data = "raise_clan_member_{}".format(
                member_id)

            btn_kick_member.text = "кикнуть"
            btn_kick_member.callback_data = "kick_clan_member_{}".format(
                member_id)

            keyboard.row(btn_raise_member, btn_kick_member)
        if member_id == member.id:
            btn_leave = copy.deepcopy(self.btn)
            btn_leave.text = "покинуть клан"
            btn_leave.callback_data = "leave_clan"
            keyboard.add(btn_leave)

        keyboard.add(keyboards.clan.btn_back_members)
        return keyboard

    def create_contest_territories_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 2

        # session
        session = db_api.CreateSession()

        # table data
        clan_member: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(user_id=self.user_id).first()

        contest: tables.Contest = session.db.query(
            tables.Contest).filter(or_(
                tables.Contest.clan_id_1 == clan_member.clan_id,
                tables.Contest.clan_id_2 == clan_member.clan_id)
        ).first()

        territory_captures = list(contest.territory_captures)

        territory_indexes = [i for i, x in enumerate(territory_captures) if x is None]

        for index in territory_indexes:
            if contest.territory_owners[index] == clan_member.clan_id:
                continue
            btn = copy.deepcopy(self.btn)
            btn.text = contest.territory_names[index]
            btn.callback_data = "territory_{}".format(index)
            keyboard.insert(btn)

        session.close()

        keyboard.add(keyboards.contest.btn_back)
        return keyboard

    def create_camp_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 2

        # session
        session = db_api.CreateSession()

        # table data
        clan_member: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(user_id=self.user_id).first()

        contest: tables.Contest = session.db.query(
            tables.Contest).filter(or_(
                tables.Contest.clan_id_1 == clan_member.clan_id,
                tables.Contest.clan_id_2 == clan_member.clan_id)
        ).first()

        territory_captures = list(contest.territory_captures)
        territory_owned = [i for i in contest.territory_owners if i == clan_member.clan_id]

        for territory in contest.territory_owners:
            if territory != clan_member.clan_id:
                continue

            btn = copy.deepcopy(self.btn)
            btn.text = "🏕 {}".format(contest.territory_names[contest.territory_owners.index(territory)])
            btn.callback_data = "camp_{}".format(contest.territory_owners.index(territory))
            keyboard.insert(btn)

        session.close()

        keyboard.add(keyboards.contest.btn_back)
        return keyboard

    def create_start_capture_keyboard(self, units_count):
        keyboard = copy.deepcopy(self.keyboard)

        keyboard.add(keyboards.contest.btn_start_capture)

        btn_explore = copy.deepcopy(self.btn)
        explore_price = random.randint(int(units_count/2), units_count)
        btn_explore.text = "{} 💰 (разведка)".format(explore_price)
        btn_explore.callback_data = "explore_price_{}".format(explore_price)

        keyboard.add(btn_explore)

        keyboard.add(keyboards.contest.btn_back)
        return keyboard

    def create_technology_keyboard(self, branch_index, technology_index):
        keyboard = copy.deepcopy(self.keyboard)

        session = db_api.CreateSession()

        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=self.user_id).first()
        progress: tables.Progress = session.db.query(
            tables.Progress).filter_by(user_id=self.user_id).first()

        age: base.Age = ages.Age.get(townhall.age)
        technology: base.Technology = ages.Age.get_all_trees()[branch_index][technology_index]

        if technology.unlock_score == progress.tree[branch_index][technology_index]:
            keyboard.add(keyboards.townhall.btn_open_tech)

        elif progress.tree[branch_index][technology_index] > technology.unlock_score:
            pass
        elif technology.unlock_score != progress.tree[branch_index][technology_index]:
            keyboard.row(
                keyboards.townhall.btn_one_progress, keyboards.townhall.btn_all_progress,
            )

        keyboard.add(keyboards.townhall.btn_back_progress)
        session.close()
        return keyboard

    def create_upgrade_clan_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)

        session = db_api.CreateSession()

        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=self.user_id).first()
        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()

        upgrade_price = [i * buildings.clan_building_lvl for i in clan_building.clan_building.upgrade_price]
        upgrade_price = transaction.Purchase.get_price(upgrade_price)
        btn = copy.deepcopy(self.btn)
        btn.text = "🔨✨ Улучшить ({})".format(upgrade_price)
        btn.callback_data = "upgrade_clan_building"

        keyboard.add(btn)
        keyboard.add(keyboards.buildings.btn_back_buildings)

        session.close()
        return keyboard


class PaginationKeyboard(BaseKeyboard):
    @staticmethod
    def paginate(data: typing.Iterable, page: int = 0, limit: int = 10) -> typing.Iterable:
        return data[page * limit:page * limit + limit]

    @staticmethod
    def get_left_page(paginated_data: list, page: int) -> int:
        page -= 1

        if page < 0:
            page = len(paginated_data)-1

        return page

    @staticmethod
    def get_right_page(paginated_data: list, page: int) -> int:
        page += 1
        if page > len(paginated_data)-1:
            page = 0

        return page

    def create_buildings_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 5

        session = db_api.CreateSession()

        # table data
        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()

        progress: tables.Progress = session.db.query(
            tables.Progress).filter_by(user_id=self.user_id).first()

        all_buildings = ages.Age.get_all_buildings()

        list_buttons = []

        for building in enumerate(buildings.buildings):
            building_pos = building[0]
            building_num = building[1]

            btn = copy.deepcopy(self.btn)

            if building_num is None:
                btn.text = "+"
                btn.callback_data = "building_pos_{}".format(building_pos)
            elif building_num == "tree":
                btn.text = "🌲"
                btn.callback_data = "tree_pos_{}".format(building_pos)
            else:
                emoji = re.findall(r"(\W+)\s+", all_buildings[building_num].name)[0]
                btn.text = emoji
                btn.callback_data = "building_pos_{}".format(building_pos)

            for i in buildings.build_timer:
                time_left = timer.Timer.get_left_time(i["timer"])
                if building_pos == i["build_pos"]:
                    btn.text = "{}{}".format(*time_left)
                    btn.callback_data = "None"

            list_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.btn)
        right_btn_mv = copy.deepcopy(self.btn)

        list_paginated_buttons = []

        for i in range(0, len(buildings.buildings)):
            btn = self.paginate(data=list_buttons, page=i, limit=25)
            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv.text = "⊲"

        left_btn_mv.callback_data = "building_page_{}".format(
            self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.text = "⊳"
        right_btn_mv.callback_data = "building_page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        for btn in list_paginated_buttons[page]:
            keyboard.insert(btn)

        keyboard.row(
            left_btn_mv,
            right_btn_mv
        )
        return keyboard

    def create_manufacture_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)

        session = db_api.CreateSession()

        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=self.user_id).first()

        manufacture: tables.Manufacture = session.db.query(
            tables.Manufacture).filter_by(user_id=self.user_id).first()

        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()
        all_buildings = ages.Age.get_all_buildings()
        all_products = ages.Age.get_all_products()
        age: base.Age = ages.Age.get(townhall.age)

        for building in enumerate(buildings.buildings):
            building_pos = building[0]
            building_num = building[1]

            btn = copy.deepcopy(self.btn)

            if building_num is None or type(building_num) is str:
                continue

            if type(all_buildings[building_num]) is base.ManufactureBuilding:
                btn.text = all_buildings[building_num].name
                btn.callback_data = "building_manufacture_pos_{}".format(building_pos)
            else:
                continue

            for queue in manufacture.creation_queue:
                time_left = timer.Timer.get_left_time(queue["timer"])
                if building_pos == queue["building_pos"]:
                    product: base.ManufactureProduct = all_products[queue["product_id"]]
                    product_emoji = re.findall(r"(\W+)\s+", product.name)[0]
                    btn.text = "{} {}{}".format(product_emoji, *time_left)
                    btn.callback_data = "None"

            for queue in manufacture.wait_queue:
                if building_pos == queue["building_pos"]:
                    product: base.ManufactureProduct = all_products[queue["product_id"]]
                    product_emoji = re.findall(r"(\W+)\s+", product.name)[0]
                    btn.text = "{} собрать".format(product_emoji)
                    btn.callback_data = "manufacture_product_{}".format(queue["product_id"])

            keyboard.add(btn)

        return keyboard

    def create_unlocked_buildings_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 5

        session = db_api.CreateSession()

        progress: tables.Progress = session.db.query(
            tables.Progress).filter_by(user_id=self.user_id).first()

        # table data
        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()

        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=self.user_id).first()

        age: base.Age = ages.Age.get(townhall.age)
        all_buildings = ages.Age.get_all_buildings()

        list_buttons = []

        for unlocked_building in progress.unlocked_buildings:
            building = all_buildings[unlocked_building]
            btn = copy.deepcopy(self.btn)
            btn.text = building.name
            btn.callback_data = "build_info_{}".format(unlocked_building)
            list_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.btn)
        right_btn_mv = copy.deepcopy(self.btn)

        list_paginated_buttons = []
        for i in range(0, len(progress.unlocked_buildings)):
            btn = self.paginate(data=list_buttons, page=i, limit=8)
            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv.text = "⊲"
        left_btn_mv.callback_data = "unlocked_buildings_page_{}".format(
            self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.text = "⊳"
        right_btn_mv.callback_data = "unlocked_buildings_page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        for btn in list_paginated_buttons[page]:
            keyboard.add(btn)

        keyboard.row(
            left_btn_mv,
            keyboards.buildings.btn_back_buildings,
            right_btn_mv
        )

        return keyboard

    def create_territory_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)
        list_values = [1, 8, 16, 32, 64, 128, 256, 512, 1028]
        list_buttons = []
        for i in list_values:
            btn = copy.deepcopy(self.btn)
            btn.text = "+{} 💂".format(i)
            btn.callback_data = "select_units_{}".format(i)

            list_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.btn)
        right_btn_mv = copy.deepcopy(self.btn)

        list_paginated_buttons = []
        for i in range(0, len(list_values)):

            btn = self.paginate(data=list_buttons, page=i, limit=1)

            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv.text = "⊲"
        left_btn_mv.callback_data = "page_{}".format(
            self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.text = "⊳"
        right_btn_mv.callback_data = "page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        keyboard.row(
            left_btn_mv,
            *list_paginated_buttons[page],
            right_btn_mv
        )
        keyboard.add(keyboards.campaigns.btn_next)
        # keyboard.add(keyboards.campaigns.btn_back_territory)

        return keyboard

    def create_market_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)

        session = db_api.CreateSession()

        market_table: typing.List[tables.Market] = session.db.query(
            tables.Market).all()

        list_buttons = []
        for index in range(0, len(market_table)):

            time_left = timer.Timer.get_left_time(market_table[index].timer)
            if time_left[0] == 0:
                session.db.query(tables.Market).filter_by(
                    id=market_table[index].id
                ).delete()
                session.db.commit()
                continue

            btn = copy.deepcopy(self.btn)
            btn.text = "x{} {} - {} 💰".format(
                market_table[index].count,
                market_table[index].product,
                market_table[index].price
            )
            btn.callback_data = "market_product_{}".format(market_table[index].id)
            list_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.btn)
        right_btn_mv = copy.deepcopy(self.btn)

        list_paginated_buttons = []
        for i in range(0, len(market_table)):

            btn = self.paginate(data=list_buttons, page=i, limit=8)

            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv.text = "⊲"
        left_btn_mv.callback_data = "market_page_{}".format(self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.text = "⊳"
        right_btn_mv.callback_data = "market_page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        if not list_buttons:
            keyboard.add(keyboards.market.btn_my_products)
            return keyboard, 1

        for btn in list_paginated_buttons[page]:
            keyboard.add(btn)

        keyboard.row(
            left_btn_mv,
            keyboards.market.btn_my_products,
            right_btn_mv
        )
        session.close()

        return keyboard, len(list_paginated_buttons)

    def create_user_products_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)

        session = db_api.CreateSession()

        market_table: typing.List[tables.Market] = session.db.query(
            tables.Market).filter_by(user_id=self.user_id).all()

        if not market_table:
            keyboard.add(keyboards.market.btn_back_market)
            return keyboard

        list_buttons = []
        for index in range(0, len(market_table)):

            btn = copy.deepcopy(self.btn)
            btn.text = "{} {} - {} 💰".format(
                market_table[index].count,
                market_table[index].product,
                market_table[index].price
            )
            btn.callback_data = "product_{}".format(market_table[index].id)
            list_buttons.append(btn)

        list_paginated_buttons = []
        for i in range(0, len(market_table)):

            btn = self.paginate(data=list_buttons, page=i, limit=8)

            if not btn:
                break

            list_paginated_buttons.append(btn)

        for btn in list_paginated_buttons[page]:
            keyboard.add(btn)

        keyboard.add(keyboards.market.btn_back_market)
        session.close()

        return keyboard

    def create_invitation_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)

        session = db_api.CreateSession()

        clan_invitations_table: typing.List[tables.ClanInvitation] = session.\
            db.query(tables.ClanInvitation).filter_by(user_id=self.user_id).join(
            tables.Clan).order_by(desc(tables.Clan.rating)).all()

        if not clan_invitations_table:
            keyboard.add(keyboards.clan.btn_back)
            return keyboard

        list_buttons = []
        for invitation in clan_invitations_table:
            time_left = timer.Timer.get_left_time(invitation.timer)

            if time_left[0] < 0:
                session.db.query(tables.ClanInvitation).filter_by(
                    id=invitation.id).delete()
                session.db.commit()
                continue

            btn = copy.deepcopy(self.btn)
            btn.text = "{} [ {} ⭐ ]".format(
                invitation.clan.name, invitation.clan.rating
            )
            btn.callback_data = "open_invitation_{}".format(invitation.id)
            list_buttons.append(btn)

        list_paginated_buttons = []
        for i in range(0, len(clan_invitations_table)):

            btn = self.paginate(data=list_buttons, page=i, limit=8)

            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.left_btn_mv)
        right_btn_mv = copy.deepcopy(self.right_btn_mv)

        left_btn_mv.callback_data = "invitation_page_{}".format(
            self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.callback_data = "invitation_page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        if not list_buttons:
            keyboard.add(keyboards.clan.btn_back)
            return keyboard, 1

        for btn in list_paginated_buttons[page]:
            keyboard.add(btn)

        keyboard.row(
            left_btn_mv,
            right_btn_mv
        )

        keyboard.add(keyboards.clan.btn_back)
        session.close()

        return keyboard

    def create_members_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)

        session = db_api.CreateSession()

        clan_member_table: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(user_id=self.user_id).first()

        clan_members_table: typing.List[tables.ClanMember] = session.db.query(
            tables.ClanMember).filter_by(clan_id=clan_member_table.clan_id).all()

        list_buttons = []
        for member in clan_members_table:
            user_table: tables.User = session.filter_by_user_id(
                user_id=member.user_id, table=tables.User)

            btn = copy.deepcopy(self.btn)
            btn.text = "{}".format(
                user_table.first_name
            )
            btn.callback_data = "check_clan_member_{}".format(member.id)
            list_buttons.append(btn)

        list_paginated_buttons = []
        for i in range(0, len(clan_members_table)):

            btn = self.paginate(data=list_buttons, page=i, limit=8)

            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.left_btn_mv)
        right_btn_mv = copy.deepcopy(self.right_btn_mv)

        left_btn_mv.callback_data = "invitation_page_{}".format(
            self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.callback_data = "invitation_page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        if not list_buttons:
            keyboard.add(keyboards.clan.btn_back)
            return keyboard

        for btn in list_paginated_buttons[page]:
            keyboard.add(btn)

        if len(list_paginated_buttons) == 1:
            keyboard.row(
                keyboards.clan.btn_back,
            )

        else:
            keyboard.row(
                left_btn_mv,
                keyboards.clan.btn_back,
                right_btn_mv
            )

        session.close()

        return keyboard

    def create_campaign_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 2

        # session
        session = db_api.CreateSession()

        # table data
        campaign: tables.Campaign = session.db.query(
            tables.Campaign).filter_by(user_id=self.user_id).first()

        base_campaigns = ages.Age.get_all_campaigns()
        territory_owners = list(campaign.territory_owned)
        not_owned_territories = [i for i, x in enumerate(territory_owners) if x is False]
        list_buttons = []

        for index in not_owned_territories:
            btn = copy.deepcopy(self.btn)
            territory = base_campaigns[index]
            btn.text = "{} | x{} 🥷 / x{} 🌲".format(
                territory.name, sum(territory.units_count), territory.territory_size
            )
            btn.callback_data = "campaign_territory_{}".format(index)
            list_buttons.append(btn)

        list_paginated_buttons = []
        for i in range(0, len(base_campaigns)):

            btn = self.paginate(data=list_buttons, page=i, limit=4)

            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.left_btn_mv)
        right_btn_mv = copy.deepcopy(self.right_btn_mv)

        left_btn_mv.callback_data = "campaign_page_{}".format(
            self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.callback_data = "campaign_page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        if not list_buttons:
            keyboard.add(keyboards.campaigns.btn_back_campaign)
            return keyboard

        for btn in list_paginated_buttons[page]:
            keyboard.add(btn)

        if len(list_paginated_buttons) == 1:
            keyboard.row(
                keyboards.clan.btn_back,
            )

        else:
            keyboard.row(
                left_btn_mv,
                keyboards.campaigns.btn_back_campaign,
                right_btn_mv
            )

        session.close()

        return keyboard

    def create_progress_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 3

        session = db_api.CreateSession()

        # tables data
        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=self.user_id).first()
        progress: tables.Progress = session.db.query(
            tables.Progress).filter_by(user_id=self.user_id).first()

        age: base.Age = ages.Age.get(townhall.age)
        progress_tree = ages.Age.get_all_trees()
        list_buttons = []

        for branch in progress_tree[:len(progress.tree)]:

            branch_index = progress_tree.index(branch)
            db_branch = list(progress.tree[branch_index])

            for value in branch:
                value: base.Technology

                value_index = branch.index(value)
                db_value = db_branch[value_index]

                btn = copy.deepcopy(self.btn)
                if value is None:
                    btn.text = "ᅠ"
                else:
                    emoji = re.findall(r"(\W+)\s+", value.name)[0]
                    if db_value > value.unlock_score:
                        btn.text = "{} (⭐)".format(emoji, db_value-1, value.unlock_score)
                    else:
                        btn.text = "{} ({}/{})".format(emoji, db_value, value.unlock_score)

                    btn.callback_data = "technology_{}_{}".format(branch_index, value_index)
                list_buttons.append(btn)
                # keyboard.insert(btn)

            # keyboard.row()
            for i in branch:
                btn = copy.deepcopy(self.btn)
                if i is None:
                    btn.text = "ᅠ"
                else:
                    btn.text = "↓"

                list_buttons.append(btn)
                # keyboard.insert(btn)
            # keyboard.row()

        list_paginated_buttons = []

        ages_progress_tree = ages.Age.get_ages_trees()

        prev_slice = 0

        for i in range(0, len(ages_progress_tree)):
            limit = []

            for x in ages_progress_tree[i]:
                limit += x

            slice = len(limit)*2 + prev_slice

            btn = list_buttons[prev_slice:slice]

            prev_slice = 0
            prev_slice += slice

            if not btn:
                break

            list_paginated_buttons.append(btn)

        left_btn_mv = copy.deepcopy(self.left_btn_mv)
        right_btn_mv = copy.deepcopy(self.right_btn_mv)
        left_btn_mv.text = "▲"
        right_btn_mv.text = "▼"

        left_btn_mv.callback_data = "tree_page_{}".format(
            self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.callback_data = "tree_page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        if len(list_paginated_buttons) > 1:
            keyboard.row(left_btn_mv)
            keyboard.row()

        for btn in list_paginated_buttons[page]:
            keyboard.insert(btn)

        list_ages = ages.Age.get_all_ages()
        next_age_name = list_ages[list_ages.index(townhall.age)+1]

        btn_next_age = copy.deepcopy(self.btn)
        btn_next_age.text = "🌟 {}".format(next_age_name)
        btn_next_age.callback_data = "unlock_age"

        keyboard.add(btn_next_age)
        keyboard.row(keyboards.townhall.btn_back_townhall)
        session.close()
        return keyboard
