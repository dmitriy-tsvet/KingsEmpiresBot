import time
from utils.db_api import db_api, tables
from utils.models import models, ages, base
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
    def get_left_time_sec(set_time: int) -> int:
        if set_time is None:
            return 0

        time_left_sec = int(set_time - time.time())

        if time_left_sec < 0:
            return 0

        return time_left_sec

    @staticmethod
    def get_left_time_min(set_time_sec: int) -> tuple:
        time_left = Timer.get_left_time(int(time.time() + set_time_sec))
        return time_left

    @staticmethod
    def get_time_passed_sec(set_time_sec, time_left_sec: int) -> int:
        return set_time_sec - time_left_sec

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


class BuildingTimer(Timer):
    def get_build_timer(self, user_id):

        session = db_api.CreateSession()
        townhall: tables.TownHall = session.db.query(
            tables.TownHall).filter_by(user_id=user_id).first()

        buildings: tables.Buildings = session.db.query(
            tables.Buildings).filter_by(user_id=user_id).first()
        base_buildings = ages.Age.get_all_buildings()

        build_timer = list(buildings.build_timer)
        for i in buildings.build_timer:

            time_left = self.get_left_time(i["timer"])

            if i.get("build_num") is None:
                if time_left[0] == 0:
                    build_timer.remove(i)
                    buildings.build_timer = build_timer
                continue

            build_num = i["build_num"]
            build_pos = i["build_pos"]

            if time_left[0] == 0:
                if type(base_buildings[build_num]) is base.HomeBuilding:
                    townhall.population += base_buildings[build_num].capacity

                crnt_buildings = list(buildings.buildings)
                crnt_buildings[build_pos] = build_num
                build_timer.remove(i)
                buildings.buildings = crnt_buildings
                buildings.build_timer = build_timer

        session.close()


class ManufactureTimer(Timer):
    def get_creation_queue(self, user_id):
        session = db_api.CreateSession()
        manufacture: tables.Manufacture = session.db.query(
            tables.Manufacture).filter_by(user_id=user_id).first()

        creation_queue = list(manufacture.creation_queue)
        wait_queue = list(manufacture.wait_queue)
        for queue in creation_queue:
            time_left = self.get_left_time(queue["timer"])

            if time_left[0] == 0:
                creation_queue.remove(queue)
                wait_queue.append(queue)

                manufacture.wait_queue = wait_queue
                manufacture.creation_queue = creation_queue
                session.db.commit()

        session.close()

    def get_wait_queue(self, user_id, product_id):
        session = db_api.CreateSession()
        manufacture: tables.Manufacture = session.db.query(
            tables.Manufacture).filter_by(user_id=user_id).first()

        wait_queue = list(manufacture.wait_queue)
        player_products = list(manufacture.storage)
        for queue in wait_queue:
            time_left = self.get_left_time(queue["timer"])
            added_products = []

            if time_left[0] == 0:
                added_products.append(queue)

                products_id = []
                for product in player_products:
                    if product["product_id"] == product_id:
                        new_product = {
                            "product_id": product_id,
                            "count": product["count"]+1
                        }
                        index = player_products.index(product)
                        player_products.remove(product)
                        player_products.insert(index, new_product)
                    products_id.append(product["product_id"])

                if product_id not in products_id:
                    player_products.append({
                            "product_id": product_id,
                            "count": 1
                        })
                wait_queue.remove(queue)

                manufacture.storage = player_products
                manufacture.wait_queue = wait_queue
                session.db.commit()

        session.close()


class HomeBuildingTimer(Timer):
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


class CampaignTimer:
    def get_capture_timer(self, user_id):
        session = db_api.CreateSession()
        campaign: tables.Campaign = session.db.query(
            tables.Campaign).filter_by(user_id=user_id).first()
        if not campaign.territory_captures:
            return

        time_left = Timer.get_left_time(campaign.territory_captures["timer"])
        if time_left[0] == 0:
            if campaign.territory_captures["win"]:
                index = campaign.territory_captures["territory_index"]
                territory_owners = list(campaign.territory_owners)
                territory_owners[index] = True
                campaign.territory_owners = territory_owners

            campaign.territory_captures = {}

        session.close()


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

    def get_creation_queue_timer(self, user_id):
        session = db_api.CreateSession()
        units: tables.Units = session.db.query(
            tables.Units).filter_by(user_id=user_id).first()

        base_units = ages.Age.get_all_units()
        creation_queue = list(units.creation_queue)
        units_count = list(units.units_count)
        for queue in creation_queue:
            queue_index = creation_queue.index(queue)

            unit_num = queue["unit_num"]
            creation_count = queue["creation_count"]
            unit = base_units[units.units_type[unit_num]]
            time_left = self.get_left_time_sec(queue["timer"])

            time_passed = self.get_time_passed_sec(
                set_time_sec=unit.create_time_sec*creation_count,
                time_left_sec=time_left
            )
            created_count = int(time_passed / unit.create_time_sec)
            units_count[unit_num] += created_count
            if created_count > 0:
                units.real_units_count += unit.weight * created_count

            units.units_count = units_count

            creation_count -= created_count
            queue["timer"] = self.set_timer(creation_count*unit.create_time_sec)

            if creation_count <= 0:
                creation_queue.remove(queue)
            else:
                new_queue = {
                    "unit_num": unit_num,
                    "creation_count": creation_count,
                    "timer": queue["timer"]
                }
                creation_queue.remove(queue)
                creation_queue.insert(queue_index, new_queue)
            units.creation_queue = creation_queue

        session.close()



