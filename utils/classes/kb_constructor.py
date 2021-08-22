import keyboards
from utils.ages import ages_list
from aiogram import types
from utils.db_api import db_api, tables
from utils.ages import models
from utils.classes import timer
import copy
import re
import json
import typing

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


class StandardKeyboard(BaseKeyboard):
    def create_townhall_keyboard(self, age):
        keyboard = copy.deepcopy(self.keyboard)

        list_of_ages = ages_list.AgesList.get_list_ages()

        if age == list_of_ages[0]:
            keyboard.row(keyboards.townhall.btn_get_tax, keyboards.townhall.btn_get_food)
        elif age in list_of_ages[1:7]:
            keyboard.add(keyboards.townhall.btn_get_tax)
            keyboard.row(keyboards.townhall.btn_get_food, keyboards.townhall.btn_get_stock)
        elif age in list_of_ages[8:14]:
            keyboard.add(keyboards.townhall.btn_get_tax)
            keyboard.row(
                keyboards.townhall.btn_get_food,
                keyboards.townhall.btn_get_stock,
                keyboards.townhall.btn_get_energy)
        elif age in list_of_ages[15:]:
            keyboard.add(keyboards.townhall.btn_get_tax)
            keyboard.row(
                keyboards.townhall.btn_get_food,
                keyboards.townhall.btn_get_stock,
            )
            keyboard.row(
                keyboards.townhall.btn_get_energy,
                keyboards.townhall.btn_get_graviton
            )
        keyboard.add(keyboards.townhall.btn_population)
        keyboard.add(keyboards.townhall.btn_progress)
        return keyboard

    def create_buildings_keyboard(self, age):
        keyboard = copy.deepcopy(self.keyboard)
        age_model: models.Age = ages_list.AgesList.get_age_model(age)

        buildings = [
            age_model.home_building,
            age_model.food_building,
            age_model.stock_building,
            age_model.energy_building,
            age_model.graviton_building
        ]
        list_btns = [
            keyboards.buildings.btn_home_buildings,
            keyboards.buildings.btn_food_buildings,
            keyboards.buildings.btn_stock_buildings,
            keyboards.buildings.btn_energy_buildings,
            keyboards.buildings.btn_graviton_buildings,
        ]

        for index in range(0, 5):
            btn = list_btns[index]
            building = buildings[index]
            if building is None:
                continue
            keyboard.add(btn)

        return keyboard

    def create_some_buildings_keyboard(
            self, table_model,
            building_model: models.Building):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 2

        session = db_api.Session(user_id=self.user_id)
        session.open_session()
        townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)

        some_buildings: table_model = session.built_in_query(table_model)
        buildings_str = str(some_buildings)

        levels = list(some_buildings.levels)

        for num_building in range(0, some_buildings.count_buildings):
            new_btn = copy.deepcopy(self.btn)
            building_emoji = re.findall(r"(\W)\s", building_model.name)[0]

            if (some_buildings.build_timer is not None) and (
                    num_building == some_buildings.build_num):

                time_left = timer.BuildingsTimer().get_build_timer(some_buildings)
                new_btn.text = "🔨👷 ({} {})".format(*time_left)
                new_btn.callback_data = "None"

            else:
                new_btn.text = "{}🏠 ({} ур.)".format(
                    building_emoji,
                    levels[num_building]
                )
                new_btn.callback_data = "check_{}_building_{}".format(buildings_str, num_building)

            keyboard.insert(new_btn)

        for num_building in range(some_buildings.count_buildings, 4):
            new_btn = copy.deepcopy(self.btn)
            new_btn.text = "+"
            new_btn.callback_data = "add_{}_building_{}".format(buildings_str, num_building)

            keyboard.insert(new_btn)

        keyboard.add(keyboards.buildings.btn_back_buildings)
        session.close_session()

        return keyboard

    def create_homes_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 6

        session = db_api.Session(user_id=self.user_id)
        session.open_session()

        citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)
        townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
        age = townhall_table.age

        home_model = ages_list.AgesList.get_age_model(age).home_building

        for num_building in range(0, citizens_table.home_counts):
            new_btn = copy.deepcopy(self.btn)
            if (citizens_table.build_timer is not None) and (
                    num_building == citizens_table.build_num):
                time_left = timer.HomeBuildingsTimer().get_build_timer(
                    citizens_table, home_model)

                new_btn.text = "🔨"
                new_btn.callback_data = "home_build_time"

            else:
                new_btn.text = " {} ".format(home_model.name)
                new_btn.callback_data = "home_{}".format(num_building)

            self.rows[0].append(new_btn)

        for num_building in range(citizens_table.home_counts, 36):

            new_btn = copy.deepcopy(self.btn)
            new_btn.text = " + "
            new_btn.callback_data = "add_home_{}".format(num_building)

            self.rows[0].append(new_btn)

        for i in range(0, len(self.rows[0])):
            keyboard.insert(self.rows[0][i])

        keyboard.add(keyboards.buildings.btn_back_buildings)
        session.close_session()

        return keyboard

    def create_units_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 5

        # session
        session = db_api.Session(user_id=self.user_id)
        session.open_session()

        get_timer = timer.UnitsTimer()

        # table data
        units_table: tables.Units = session.built_in_query(tables.Units)
        unit_counts = units_table.unit_counts

        townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
        age = townhall_table.age

        # age model
        units_model: tuple = ages_list.AgesList.get_age_model(age).units

        for i in range(0, 5):   # first row
            new_btn = copy.deepcopy(self.btn)

            if (units_table.upgrade_timer is not None) and (
                    i == units_table.unit_num):
                new_btn.text = "🔨"
                new_btn.callback_data = "unit_upgrading"

            elif i > len(units_model)-1:
                new_btn.text = "🔒"
                new_btn.callback_data = "unit_locked"
            else:
                emoji_unit = re.findall(r"(\W)\s", units_model[i].name)[0]
                new_btn.text = "{} {}".format(unit_counts[i], emoji_unit)
                new_btn.callback_data = "check_unit_{}".format(i)

            self.rows[0].append(new_btn)

        for i in range(0, 5):   # second row
            new_btn = copy.deepcopy(self.btn)

            if (units_table.upgrade_timer is not None) and (
                    i == units_table.unit_num):
                new_btn.text = "⏱"
                new_btn.callback_data = "unit_upgrading"
                get_timer.get_upgrade_timer(units_table)

            elif i > len(units_model)-1:
                new_btn.text = "—"
                new_btn.callback_data = "unit_locked"
            else:
                new_btn.text = "+"
                new_btn.callback_data = "create_unit_{}".format(i)

            self.rows[1].append(new_btn)

        keyboard.row(*self.rows[0])
        keyboard.row(*self.rows[1])

        session.close_session()
        return keyboard

    def create_territory_keyboard(self):
        keyboard = copy.deepcopy(self.keyboard)
        keyboard.row_width = 2

        # session
        session = db_api.Session(user_id=self.user_id)
        session.open_session()

        # table data
        territory_table: tables.Territory = session.built_in_query(tables.Territory)
        owned_territory = list(territory_table.owned_territory)
        indexes_owned_territory = [i for i, x in enumerate(owned_territory) if x is True]

        townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)
        age = townhall_table.age

        age_model: models.Age = ages_list.AgesList.get_age_model(age)
        models_territories: typing.List[models.Territory] = age_model.territories

        for territory in models_territories:
            index = models_territories.index(territory)

            if index in indexes_owned_territory:
                continue

            btn = copy.deepcopy(self.btn)
            btn.text = territory.name
            btn.callback_data = "territory_{}".format(index)
            keyboard.insert(btn)

        keyboard.add(keyboards.territory.btn_back_territory)
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

    def create_citizens_keyboard(self, page: int = 0):
        keyboard = copy.deepcopy(self.keyboard)

        list_values = [1, 8, 16, 32, 64, 128, 256, 512, 1028]
        list_buttons = []
        for i in list_values:
            btn = copy.deepcopy(self.btn)
            btn.text = "+{} 👨🏼‍🌾".format(i)
            btn.callback_data = "create_people_{}".format(i)

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
        left_btn_mv.callback_data = "page_{}".format(self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.text = "⊳"
        right_btn_mv.callback_data = "page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        keyboard.add(keyboards.citizens.btn_info)
        keyboard.row(
            left_btn_mv,
            *list_paginated_buttons[page],
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
        left_btn_mv.callback_data = "page_{}".format(self.get_left_page(list_paginated_buttons, page))

        right_btn_mv.text = "⊳"
        right_btn_mv.callback_data = "page_{}".format(
            self.get_right_page(list_paginated_buttons, page))

        keyboard.row(
            left_btn_mv,
            *list_paginated_buttons[page],
            right_btn_mv
        )
        keyboard.add(keyboards.territory.btn_next)
        keyboard.add(keyboards.territory.btn_back_territory)

        return keyboard


