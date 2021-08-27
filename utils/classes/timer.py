import time
from utils.db_api import db_api, tables
from utils.ages import models
from utils.classes import maths
import json
import typing
import random
from utils.misc.operation_with_lists import subtract_nums_list, add_nums_list

class Timer:

    @staticmethod
    def get_left_time(set_time: int) -> tuple:
        if set_time is None:
            return 0, "сек."

        time_left_sec = int(set_time - time.time())
        time_left_min = int(time_left_sec / 60)
        time_left_hour = int(time_left_min / 60)

        if time_left_sec < 0:
            return 0, "сек."

        if time_left_sec < 60:
            return time_left_sec, "сек."
        elif time_left_min < 60:
            return time_left_min, "мин."
        elif time_left_min >= 60:
            time_left_min = time_left_min % 60
            time_left_hour = float(
                "{}.{}".format(time_left_hour, time_left_min)
            )
            return time_left_hour, "ч."

    @staticmethod
    def get_time_passed_min(time_left: tuple) -> int:
        time_passed = 0

        if time_left[1] == "сек.":
            time_passed = 60
        elif time_left[1] == "мин.":
            time_passed = 60 - time_left[0]

        return time_passed

    @staticmethod
    def set_income_timer(table):
        set_time = int(time.time() + 3600)
        table.timer = set_time

    @staticmethod
    def set_upgrade_timer(table, table_model):
        set_time = int(time.time() + table_model.upgrade_time_sec)
        table.upgrade_timer = set_time

    @staticmethod
    def set_build_timer(table, table_model):
        set_time = int(time.time() + table_model.create_time_sec)
        table.build_timer = set_time

    @staticmethod
    def set_timer(time_in_sec):
        set_time = int(time.time() + time_in_sec)
        return set_time


class MoneyTimer(Timer):

    def get_money_timer(self, townhall_table, citizen_table) -> int:
        set_time = townhall_table.timer

        time_left = self.get_left_time(set_time)

        income = int(citizen_table.population * 2)
        income_min = income / 60

        time_passed = self.get_time_passed_min(time_left)
        if time_passed <= 1:
            money_income = 0
        else:
            money_income = int(time_passed * income_min)

        self.set_income_timer(townhall_table)

        return money_income


class BuildingsTimer(Timer):

    async def get_resource_timer(self, buildings_table, building) -> int:
        building_efficiency = building.efficiency
        set_time = buildings_table.timer

        lvl_buff = building.get_lvl_buff(buildings_table)

        time_left = self.get_left_time(set_time)

        income_min = building_efficiency / 60

        time_passed = self.get_time_passed_min(time_left)
        if time_passed <= 1:
            resource_income = 0
        else:
            resource_income = (time_passed * income_min) * lvl_buff

        resource_income = int(resource_income)
        self.set_income_timer(buildings_table)

        return resource_income

    def get_build_timer(self, some_buildings):
        set_time = some_buildings.build_timer
        levels = list(some_buildings.levels)
        build_num = some_buildings.build_num

        time_left = self.get_left_time(set_time)

        if time_left[0] == 0:
            levels[build_num] += 1
            some_buildings.levels = levels
            some_buildings.build_timer = None
            some_buildings.build_num = None
            return 0, "сек."
        else:
            return time_left


class HomeBuildingsTimer(Timer):

    def get_build_timer(self, citizens_table, home_model):
        set_time = citizens_table.build_timer
        time_left = self.get_left_time(set_time)

        if time_left[0] == 0:
            citizens_table.capacity += home_model.capacity
            citizens_table.home_counts += 1
            citizens_table.build_timer = None
            citizens_table.build_num = None
            return 0, "сек."
        else:
            return time_left


class UnitsTimer(Timer):
    def get_upgrade_timer(self, units_table):
        set_time = units_table.upgrade_timer
        levels = list(units_table.levels)
        num_unit = units_table.unit_num

        time_left = self.get_left_time(set_time)

        if time_left[0] == 0:
            levels[num_unit] += 1
            units_table.levels = levels
            units_table.upgrade_timer = None
            units_table.unit_num = None
            return 0, "сек."
        else:
            return time_left

    @staticmethod
    def get_create_time_left(seconds):
        if seconds < 60:
            return seconds, "сек."
        elif seconds >= 60:
            create_time = int(seconds / 60)
            return create_time, "мин."

    @staticmethod
    def set_create_timer(units_table, num_unit: int, model_unit, creation_count: int = 1):
        creation_queue = list(units_table.creation_queue)
        creation_timer = list(units_table.creation_timer)

        weight = model_unit.get_current_weight(units_table.levels[num_unit])
        create_time_sec = model_unit.create_time_sec

        time_left_sec = int(creation_timer[num_unit] - time.time())
        if time_left_sec < 0:
            time_left_sec = 0

        set_time = int(time.time() + ((create_time_sec * creation_count) + time_left_sec))

        creation_queue[num_unit] += (weight * creation_count)
        creation_timer[num_unit] = set_time

        units_table.creation_queue = creation_queue
        units_table.creation_timer = creation_timer

    def get_create_timer(self, units_table):
        creation_queue = list(units_table.creation_queue)
        creation_timer = list(units_table.creation_timer)
        unit_counts = list(units_table.unit_counts)

        for i in creation_timer:
            time_left = self.get_left_time(i)
            index = creation_timer.index(i)

            if time_left[0] == 0:
                units_table.all_unit_counts += int(creation_queue[index])
                unit_counts[index] += int(creation_queue[index])

                creation_timer[index] = 0
                creation_queue[index] = 0

        units_table.creation_queue = creation_queue
        units_table.creation_timer = creation_timer
        units_table.unit_counts = unit_counts


class CitizenTimer(Timer):

    @staticmethod
    def set_create_timer(
            citizens_table: tables.Citizens,
            create_time_sec: int,
            creation_count: int = 1):

        time_left_sec = int(citizens_table.creation_timer - time.time())
        if time_left_sec < 0:
            time_left_sec = 0

        set_time = int(time.time() + ((create_time_sec * creation_count) + time_left_sec))
        citizens_table.creation_timer = set_time

    @staticmethod
    def get_create_timer(citizen_table: tables.Citizens):
        time_left = Timer.get_left_time(citizen_table.creation_timer)

        if time_left[0] == 0:
            citizen_table.population += citizen_table.creation_queue

            citizen_table.creation_queue = 0
            citizen_table.creation_timer = 0

        return time_left


class TerritoryTimer(Timer):

    @staticmethod
    def get_money_timer(territory_table: tables.Territory,
                        indexes_owned_territory: list,
                        models_territories: typing.List[models.Territory]) -> int:

        set_time = territory_table.tax_timer

        time_left = Timer.get_left_time(set_time)
        income = 0

        for index in indexes_owned_territory:
            income += models_territories[index].tax

        income_min = income / 60

        time_passed = Timer.get_time_passed_min(time_left)
        if time_passed <= 1:
            money_income = 0
        else:
            money_income = int(time_passed * income_min)

        new_set_time = Timer.set_timer(3600)
        territory_table.tax_timer = new_set_time

        return money_income

    @staticmethod
    def get_capture_timer(territory_table: tables.Territory):
        time_left = Timer.get_left_time(territory_table.capture_timer)
        owned_territory = list(territory_table.owned_territory)

        if time_left[0] == 0:
            if territory_table.capture_state == "win":
                owned_territory[territory_table.capturing_index] = True
                territory_table.owned_territory = owned_territory

            territory_table.capturing_index = None
            territory_table.capture_state = None
            territory_table.capture_timer = 0

        return time_left


class FinanceTimer(Timer):
    def get_money_timer(self, finance_table, citizen_table) -> int:
        set_time = finance_table.money_timer

        time_left = self.get_left_time(set_time)

        spend = maths.Maths.subtract_percent(citizen_table.population, 70)
        spend = random.randint(0, spend)
        spend_min = (spend / 60)

        time_passed = self.get_time_passed_min(time_left)
        if time_passed <= 1:
            spend = 0
        else:
            spend = int(time_passed * spend_min)

        return spend

    def get_culture_timer(self, finance_table, citizen_table) -> int:

        spend_money = self.get_money_timer(finance_table, citizen_table)
        finance_table.culture -= spend_money

        if finance_table.culture > 0:
            return 0

        set_time = finance_table.sanction_timer
        time_left = self.get_left_time(set_time)

        if citizen_table.population < 80:
            return 0

        spend = maths.Maths.subtract_percent(citizen_table.population, 70)
        spend = random.randint(0, spend)
        spend_min = (spend / 60)

        time_passed = self.get_time_passed_min(time_left)
        if time_passed <= 1:
            spend = 0
        else:
            spend = int(time_passed * spend_min)

        time_set = self.set_timer(3600)
        finance_table.sanction_timer = time_set
        citizen_table.population -= spend

    def get_economics_timer(self, finance_table, townhall_table, citizen_table) -> int:

        spend_money = self.get_money_timer(finance_table, citizen_table)
        finance_table.economics -= spend_money

        if finance_table.economics > 0:
            return 0

        set_time = finance_table.sanction_timer
        time_left = self.get_left_time(set_time)

        if townhall_table.food < 50:
            return 0

        spend = maths.Maths.subtract_percent(townhall_table.food, 70)
        spend = random.randint(0, spend)
        spend_min = (spend / 60)

        time_passed = self.get_time_passed_min(time_left)
        if time_passed <= 1:
            spend = 0
        else:
            spend = int(time_passed * spend_min)

        time_set = self.set_timer(3600)
        finance_table.sanction_timer = time_set
        townhall_table.food -= spend

    def get_army_timer(self, finance_table, units_table, citizen_table) -> int:

        spend_money = self.get_money_timer(finance_table, citizen_table)
        finance_table.army -= spend_money

        if finance_table.army > 0:
            return 0

        set_time = finance_table.sanction_timer
        time_left = self.get_left_time(set_time)

        if units_table.all_unit_counts < 20:
            return 0

        spend = maths.Maths.subtract_percent(units_table.all_unit_counts, 70)
        spend = random.randint(0, spend)
        spend_min = (spend / 60)

        time_passed = self.get_time_passed_min(time_left)
        if time_passed <= 1:
            spend = 0
        else:
            spend = int(time_passed * spend_min)

        time_set = self.set_timer(3600)
        finance_table.sanction_timer = time_set
        units_table.all_unit_counts -= spend
        unit_counts = list(units_table.unit_counts)
        units_table.unit_counts = subtract_nums_list(spend, unit_counts)

