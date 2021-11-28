import typing
import time
from utils.db_api import db_api, tables
from utils.models import ages, base
from utils.classes import maths, timer
import json
import typing
import random
from utils.misc.operation_with_lists import subtract_nums_list, add_nums_list


class HourIncome:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_progress_score_income(self) -> int:
        session = db_api.CreateSession()

        progress: tables.Progress = session.db.query(
            tables.Progress).filter_by(user_id=self.user_id).first()

        set_time = progress.score_timer
        time_left = timer.Timer.get_left_time(set_time)

        time_passed = timer.Timer.get_time_passed_min(time_left)
        if time_passed <= 1:
            score_income = 0
        else:
            score_income = 1
            progress.score_timer = timer.Timer.set_timer(3600)

        session.close()
        return score_income

    def get_money_income(self) -> int:
        session = db_api.CreateSession()

        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=self.user_id).first()
        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()
        base_buildings = ages.Age.get_all_buildings()
        buildings_buildings = list(buildings.buildings)

        income = 0
        for building_num in buildings_buildings:
            if type(building_num) is int:
                if type(base_buildings[building_num]) is base.HomeBuilding:
                    income += base_buildings[building_num].income

        set_time = townhall.timer
        time_left = timer.Timer.get_left_time(set_time)
        income_min = income / 60

        time_passed = timer.Timer.get_time_passed_min(time_left)
        if time_passed <= 1:
            money_income = 0
        else:
            money_income = int(time_passed * income_min)
            townhall.timer = timer.Timer.set_timer(3600)

        session.close()
        return money_income

    def get_stock_income(self) -> int:
        session = db_api.CreateSession()

        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=self.user_id).first()

        set_time = buildings.timer

        base_buildings = ages.Age.get_all_buildings()
        base_stock_buildings = ages.Age.get_all_stock_buildings()
        buildings_income = 0

        for building in base_stock_buildings:
            index = base_buildings.index(building)
            stock_buildings = list(buildings.buildings)

            for i in range(0, stock_buildings.count(index)):
                buildings_income += building.efficiency
        time_left = timer.Timer.get_left_time(set_time)

        if buildings_income == 0:
            return 0

        income_min = buildings_income / 60

        time_passed = timer.Timer.get_time_passed_min(time_left)
        if time_passed <= 1:
            resource_income = 0
        else:
            resource_income = int(time_passed * income_min)

        session.close()
        return resource_income
