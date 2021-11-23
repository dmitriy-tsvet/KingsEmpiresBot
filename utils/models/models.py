import random, typing
from utils.resource_lvl_buff import resource_lvl_buff
from utils.misc.fill_in_list import fill_in_list


class Building:
    def __init__(self, name: str, resource: str, efficiency: int,
                 create_price: int, create_time_sec: int,
                 upgrade_price: int, upgrade_time_sec: int, lvl=1
                 ):
        self.name = name
        self.lvl = lvl
        self.create_price = create_price
        self.create_time_sec = create_time_sec
        self.upgrade_price = int(upgrade_price * float("1.{}".format(lvl)))
        self.upgrade_time_sec = upgrade_time_sec

    def get_all_efficiency(self, buildings_table) -> int:
        lvl_buff = self.get_lvl_buff(buildings_table)
        efficiency = float(self.efficiency * lvl_buff)
        return int(efficiency)

    def get_hour_efficiency(self, lvl) -> int:
        lvl_buff = float("1.{}".format(lvl)) - 0.1
        lvl_buff += 0.001
        efficiency = float(self.efficiency * lvl_buff)
        return int(efficiency)

    @staticmethod
    def get_lvl_buff(buildings_table) -> int:
        levels = list(buildings_table.levels)
        lvl_buff = 0

        for i in levels:
            lvl_buff += resource_lvl_buff(i)

        return lvl_buff


class StockBuilding(Building):
    def create(self, efficiency):
        self.efficiency = efficiency  # for 1 hour



class HomeBuilding:
    def __init__(self, name: str, img: str, capacity: int, create_price: int, create_time_sec: int):
        self.name = name
        self.img = "data/img/homes/{}.webp".format(img)
        self.capacity = capacity
        self.create_price = create_price
        self.create_time_sec = create_time_sec


class Citizen:
    def __init__(self, name: str, create_price: list, create_time_sec: int):
        self.name = name
        self.create_price = fill_in_list(create_price)
        self.create_time_sec = create_time_sec


class Unit:
    def __init__(self, name: str, weight: float, create_price: list,
                 create_time_sec: int, upgrade_price: list,
                 upgrade_time_sec: int, max_lvl: int, lvl=1
                 ):
        self.name = name
        self.lvl = lvl
        self.weight = weight
        self.max_lvl = max_lvl
        self.create_price = fill_in_list(create_price)
        self.create_time_sec = create_time_sec
        self.upgrade_price = [int(i * float("1.{}".format(lvl))-0.1) for i in upgrade_price]
        self.upgrade_price = fill_in_list(self.upgrade_price)
        self.upgrade_time_sec = upgrade_time_sec

    def get_current_weight(self, lvl):
        lvl_buff = float("1.{}".format(lvl))-0.1
        weight = self.weight * lvl_buff
        weight = float("{0:.1f}".format(weight))
        return weight

    def get_current_create_time(self, lvl):
        create_time = self.create_time_sec * float("1.{}".format(lvl)) - 0.1
        create_time = int(create_time)
        return create_time


class Territory:
    def __init__(self, name: str, tax: int, unit_counts: int,
                 time_capture_sec: int):
        self.name = name
        self.tax = tax
        self.unit_counts = unit_counts
        self.time_capture_sec = time_capture_sec


class Age:
    def __init__(self, name: str, next_age_price: list,
                 townhall_img: str, industrial_building: str,
                 units: typing.List[Unit], territories: list,
                 home_building: HomeBuilding, stock_building: Building = None,
                 energy_building: Building = None, graviton_building: Building = None,

                 ):
        self.name = name
        self.townhall_img = "data/img/townhalls/{}.webp".format(townhall_img)

        self.next_age_price = fill_in_list(next_age_price)

        self.home_building = home_building
        self.stock_building = stock_building
        self.manufacture_building = industrial_building

        self.units = units
        self.territories = territories
