from enum import Enum
from utils.models import base, stock_building,\
    home, unit, progress_tree, campaigns, clan_building, builder_home, manufacture_building, chest
import typing


class Age(Enum):

    stone_age: base.Age = base.Age(
        name="Каменный Век",
        townhall_img="stone",
        progress_tree=progress_tree.stone_progress_tree,
        next_age_price=[1120, ],
        buildings=[
            builder_home.builder_home,
            clan_building.clan_building,
            home.StoneHome,
            stock_building.StoneHut,
            ],
        units=[unit.StoneMilitia],
        campaigns=[i.value for i in campaigns.Campaigns]
    )

    bronze_age: base.Age = base.Age(
        name="Бронзовый Век",
        townhall_img="bronze",
        progress_tree=progress_tree.bronze_progress_tree,
        next_age_price=[1120, ],
        buildings=[
            home.BronzeHome_1,
            home.BronzeHome_2,
            home.BronzeHome_3,
            stock_building.BronzeSawmill,
            stock_building.BronzeForager,
            stock_building.BronzeWinery,
            manufacture_building.BronzePottery,
            manufacture_building.BronzePlantation
        ],
        units=[unit.BronzeSwordsman, unit.BronzeArcher],
        campaigns=[]
    )

    iron_age: base.Age = base.Age(
        name="Железный Век",
        townhall_img="iron",
        progress_tree=progress_tree.iron_progress_tree,
        next_age_price=[1120, ],
        buildings=[
            home.IronHome_1,
            home.IronHome_2,
            home.IronHome_3,
            stock_building.IronFoundry,
            stock_building.IronJewelry,
            stock_building.IronFelting,
            manufacture_building.IronForger,
            manufacture_building.IronButcher
        ],
        units=[unit.IronLegionary, None, unit.IronRider],
        campaigns=[]
    )

    early_middle_age: base.Age = base.Age(
        name="Раннее Средневековье",
        townhall_img="bronze",
        progress_tree=progress_tree.iron_progress_tree,
        next_age_price=[1120, ],
        buildings=[
            home.IronHome_1,
        ],
        units=[unit.IronLegionary, unit.IronRider],
        campaigns=[]
    )

    @staticmethod
    def get_all_ages():
        list_of_ages = list(map(lambda age: age.value.name, Age))
        return list_of_ages

    @staticmethod
    def get_all_buildings() -> list:
        all_buildings = []
        for i in Age:
            all_buildings += i.value.buildings
        return all_buildings

    @staticmethod
    def get_all_stock_buildings() -> typing.List[base.StockBuilding]:
        all_buildings = []
        for age in Age:
            for building in age.value.buildings:
                if type(building) is base.StockBuilding:
                    all_buildings.append(building)

        return all_buildings

    @staticmethod
    def get_all_units() -> typing.List[base.Unit]:
        all_units = []
        for i in Age:
            all_units += i.value.units
        return all_units

    @staticmethod
    def get_all_products() -> typing.List[base.ManufactureProduct]:

        all_buildings = Age.get_all_buildings()
        all_products = []
        for building in all_buildings:
            if type(building) is base.ManufactureBuilding:
                all_products += building.products
        return all_products

    @staticmethod
    def get_all_unlocked_products(age: str) -> typing.List[base.ManufactureProduct]:

        all_buildings = Age.get_all_buildings()
        all_products = []
        for building in all_buildings:
            if type(building) is base.ManufactureBuilding:
                all_products += building.products
        return all_products

    @staticmethod
    def get_all_campaigns() -> typing.List[base.Campaign]:

        all_campaigns = []
        for i in Age:
            all_campaigns += i.value.campaigns
        return all_campaigns

    @staticmethod
    def get(current_age: str):
        for i in Age:
            if i.value.name == current_age:
                return i.value

    @staticmethod
    def next_age_name(current_age: str):
        for i in Age:
            if i.value.name == current_age:
                return i.value

    @staticmethod
    def get_ages_trees():
        trees = []
        for i in Age:
            trees.append(i.value.progress_tree)
        return trees

    @staticmethod
    def get_all_trees():
        trees = []
        for i in Age:
            trees += i.value.progress_tree

        return trees

    @staticmethod
    def get_all_chests():

        chests = [
            chest.Caesar,
            chest.Atilla,
            chest.Barbarossa,
            chest.JoanArc,
            chest.Napoleon,
            chest.Churchill,
            chest.SteveJobs
        ]

        return chests
