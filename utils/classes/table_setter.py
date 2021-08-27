from utils.db_api import tables, db_api
from utils.ages import models, ages_list
from aiogram import types


class TableSetter:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def set_stone_age(self, message: types.Message, country_name: str):
        age: models.Age = ages_list.AgesList.get_age_model("Каменный")
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        user_mention = message.from_user.get_mention()

        units_empty_list = [
            0 for i in range(0, len(age.units))
        ]
        units_levels_list = [
            1 for i in range(0, len(age.units))
        ]

        territories_empty_list = [
            False for i in range(0, len(age.territories))
        ]

        new_session = db_api.NewSession()

        user = tables.User(
            user_id=self.user_id, first_name=first_name,
            last_name=last_name, username=username,
        )

        units = tables.Units(
            user_id=self.user_id,
            all_unit_counts=0,
            unit_counts=units_empty_list,
            creation_queue=units_empty_list,
            creation_timer=units_empty_list,
            creation_value=1,
            levels=units_levels_list,
            upgrade_timer=None,
            unit_num=None
        )

        townhall = tables.TownHall(
            user_id=self.user_id,
            country_name=country_name,
            age=age.name,
            money=0,
            timer=None,
            food=0,
            stock=0,
            energy=0,
            graviton=0
        )

        territory = tables.Territory(
            user_id=self.user_id,
            tax_timer=None,
            capture_timer=None,
            owned_territory=territories_empty_list,
            capturing_index=None,
            capture_state=None,
        )

        food_buildings = tables.FoodBuildings(
            user_id=self.user_id,
            count_buildings=1,
            levels=[1, 0, 0, 0],
            timer=None,
            build_timer=None,
            build_num=None
        )

        stock_buildings = tables.StockBuildings(
            user_id=self.user_id,
            count_buildings=1,
            levels=[1, 0, 0, 0],
            timer=None,
            build_timer=None,
            build_num=None
        )

        citizens = tables.Citizens(
            user_id=self.user_id,
            population=100,
            capacity=100,
            creation_queue=0,
            creation_timer=0,
            home_counts=1,
            build_timer=None,
            build_num=None
        )

        finance = tables.Finance(
            user_id=self.user_id,
            culture=20,
            economics=20,
            army=20,
        )

        new_session.session.add(user)
        new_session.session.add(units)
        new_session.session.add(townhall)
        new_session.session.add(territory)
        new_session.session.add(food_buildings)
        new_session.session.add(stock_buildings)
        new_session.session.add(citizens)
        new_session.session.add(finance)

        new_session.close()

    def set_next_age(self, next_age: str):

        age: models.Age = ages_list.AgesList.get_age_model(next_age)

        units_empty_list = [
            0 for i in range(0, len(age.units))
        ]

        territories_empty_list = [
            False for i in range(0, len(age.territories))
        ]

        units_levels_list = [
            1 for i in range(0, len(age.units))
        ]

        new_session = db_api.NewSession()

        units_table: tables.Units = new_session.filter_by_user_id(
            user_id=self.user_id, table=tables.Units)

        units_table.all_unit_counts = 0
        units_table.unit_counts = units_empty_list
        units_table.creation_queue = units_empty_list
        units_table.creation_timer = units_empty_list
        units_table.levels = units_levels_list
        units_table.creation_value = 1
        units_table.upgrade_timer = None
        units_table.upgrade_unit_num = None

        townhall_table: tables.TownHall = new_session.filter_by_user_id(
            user_id=self.user_id, table=tables.TownHall)
        townhall_table.age = next_age

        territory_table: tables.Territory = new_session.filter_by_user_id(
            user_id=self.user_id, table=tables.Territory)

        territory_table.tax_timer = None
        territory_table.capture_timer = None
        territory_table.owned_territory = territories_empty_list
        territory_table.capturing_index = None
        territory_table.capture_state = None

        food_buildings_table: tables.FoodBuildings = new_session.filter_by_user_id(
            user_id=self.user_id, table=tables.FoodBuildings)

        food_buildings_table.count_buildings = 1
        food_buildings_table.levels = [1, 0, 0, 0]
        food_buildings_table.build_timer = None
        food_buildings_table.build_num = None

        stock_buildings_table: tables.StockBuildings = new_session.filter_by_user_id(
            user_id=self.user_id, table=tables.StockBuildings)

        stock_buildings_table.count_buildings = 1
        stock_buildings_table.levels = [1, 0, 0, 0]
        stock_buildings_table.build_timer = None
        stock_buildings_table.build_num = None

        citizens_table: tables.Citizens = new_session.filter_by_user_id(
            user_id=self.user_id, table=tables.Citizens)

        citizens_table.home_counts = 1
        citizens_table.build_timer = None
        citizens_table.build_num = None

        new_session.close()
