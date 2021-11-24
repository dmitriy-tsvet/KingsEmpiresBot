import random, typing
from utils.resource_lvl_buff import resource_lvl_buff
from utils.misc.fill_in_list import fill_in_list


class StockBuilding:
    def __init__(self, name: str, create_price: list, create_time_sec: int,
                 efficiency: int, manpower: int):
        self.name = name
        self.create_price = create_price
        self.create_time_sec = create_time_sec
        self.efficiency = efficiency
        self.manpower = manpower

    def __str__(self):
        return "Промышленное здание"


class ManufactureProduct:
    def __init__(self, name: str, create_time_sec: int,
                 income: int):
        self.name = name
        self.income = income
        self.create_time_sec = create_time_sec


class ManufactureBuilding:
    def __init__(self, name: str, products: typing.List[ManufactureProduct],
                 create_price: list, create_time_sec: int, manpower: int
                 ):
        self.name = name
        self.products = products
        self.create_price = create_price
        self.create_time_sec = create_time_sec
        self.manpower = manpower

    def __str__(self):
        return "Производственное здание"


class BuilderHome:
    def __init__(self, name: str, create_price: list, create_time_sec: int):
        self.name = name
        self.create_price = create_price
        self.create_time_sec = create_time_sec

    def __str__(self):
        return "Уникальное здание"


class HomeBuilding:
    def __init__(self, name: str, capacity: int, income: int,
                 create_price: list, create_time_sec: int):
        self.name = name
        self.capacity = capacity
        self.income = income
        self.create_price = create_price
        self.create_time_sec = create_time_sec

    def __str__(self):
        return "Жилое здание"


class BuildingsLet:
    def __init__(self, name: str, time_sec_destroy: int):
        self.name = name
        self.time_sec_destroy = time_sec_destroy


class ClanBuilding:
    def __init__(self, name: str, fix_price: list, upgrade_price: list, capacity: int):
        self.name = name
        self.fix_price = fix_price
        self.upgrade_price = upgrade_price
        self.capacity = capacity


class Unit:
    def __init__(self, name: str, type_unit: str, damage: int, armor: int,
                 create_price: list, create_time_sec: int
                 ):
        self.name = name
        self.type_unit = type_unit
        self.damage = damage
        self.armor = armor
        self.weight = int((damage + armor) / 3)
        self.create_price = create_price
        self.create_time_sec = create_time_sec

    def get_current_weight(self, lvl):
        lvl_buff = float("1.{}".format(lvl))-0.1
        weight = self.weight * lvl_buff
        weight = float("{0:.1f}".format(weight))
        return weight

    def get_current_create_time(self, lvl):
        create_time = self.create_time_sec * float("1.{}".format(lvl)) - 0.1
        create_time = int(create_time)
        return create_time

    def __str__(self):
        return "Юнит"


class Campaign:
    def __init__(self, name: str, income: list,
                 units_count: list, units_type: list,
                 time_capture_sec: int, territory_size: int):
        self.name = name
        self.income = income
        self.units_count = units_count
        self.units_type = units_type
        self.real_units_count = sum(
            [i[1].weight*units_count[i[0]] for i in enumerate(units_type)]
        )
        self.territory_size = territory_size
        self.time_capture_sec = time_capture_sec


class Technology:
    def __init__(self, name: str, unlock_price: list, unlock_technology, unlock_score: int):
        self.name = name
        self.unlock_price = unlock_price
        self.unlock_score = unlock_score
        self.unlock_technology = unlock_technology

    def unlock(self):
        if type(self.unlock_technology) is StockBuilding:
            pass
        elif type(self.unlock_technology) is ManufactureProduct:
            pass


class ProgressTree:
    def __init__(self, tree: list):
        self.tree = tree


class Age:
    def __init__(self, name: str,
                 next_age_price: list,
                 townhall_img: str,
                 progress_tree: list,
                 buildings: typing.List[
                     typing.Union[StockBuilding, ManufactureBuilding, HomeBuilding]],
                 units: typing.List[Unit],
                 campaigns: list
                 ):
        self.name = name
        self.townhall_img = "data/img/townhalls/{}.webp".format(townhall_img)
        self.progress_tree = progress_tree
        self.next_age_price = next_age_price
        self.buildings = buildings

        self.units = units
        self.campaigns = campaigns
