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
            home.stone_home,
            stock_building.stone_hut,
            ],
        units=[unit.stone_militia],
        campaigns=[i.value for i in campaigns.Campaigns]
    )

    bronze_age: base.Age = base.Age(
        name="Бронзовый Век",
        townhall_img="bronze",
        progress_tree=progress_tree.bronze_progress_tree,
        next_age_price=[1120, ],
        buildings=[
            home.bronze_home_1,
            home.bronze_home_2,
            home.bronze_home_3,
            stock_building.bronze_sawmill,
            stock_building.bronze_forager,
            stock_building.bronze_winery,
            manufacture_building.bronze_pottery,
            manufacture_building.bronze_plantation
        ],
        units=[unit.bronze_swordsman, unit.bronze_archer],
        campaigns=[]
    )

    iron_age: base.Age = base.Age(
        name="Железный Век",
        townhall_img="iron",
        progress_tree=progress_tree.iron_progress_tree,
        next_age_price=[1120, ],
        buildings=[
            home.iron_home_1,
            home.iron_home_2,
            home.iron_home_3,
            stock_building.IronFoundry,
            stock_building.IronJewelry,
            stock_building.IronFelting,
            manufacture_building.IronForger,
            manufacture_building.IronButcher
        ],
        units=[unit.iron_legionary, None, unit.iron_rider],
        campaigns=[]
    )

    early_middle_age: base.Age = base.Age(
        name="Раннее Средневековье",
        townhall_img="bronze",
        progress_tree=progress_tree.iron_progress_tree,
        next_age_price=[1120, ],
        buildings=[
            home.iron_home_1,
        ],
        units=[unit.bronze_swordsman, unit.bronze_archer],
        campaigns=[]
    )

    # early_middle_age = models.Age(
    #     name="Раннее Средневековье",
    #     rank="Барон",
    #     townhall_img="early_middle",
    #     buildings_img=["early_middle_bakery", "early_middle_forge"],
    #     next_age_price=[7205, 2700],
    #     citizen=citizens.early_middle_citizen,
    #     home_building=homes.early_middle_home,
    #     food_building=buildings.early_middle_bakery,
    #     stock_building=buildings.early_middle_forge,
    #     units=[units.archer, units.rider],
    #     territories=[territories.muderia, territories.brovadia, territories.hitopia,  ]
    # )
    #
    # high_middle_age = models.Age(
    #     name="Высокое Средневековье",
    #     rank="Граф",
    #     townhall_img="high_middle",
    #     buildings_img=["high_middle_farm", "high_middle_herbalist"],
    #     next_age_price=[9105, 4480],
    #     citizen=citizens.high_middle_citizen,
    #     home_building=homes.high_middle_home,
    #     food_building=buildings.high_middle_farm,
    #     stock_building=buildings.high_middle_herbalist,
    #     units=[units.healer, units.mercenary],
    #     territories=[territories.muderia, territories.brovadia, territories.seligia, ]
    # )
    #
    # late_middle_age = models.Age(
    #     name="Позднее Средневековье",
    #     rank="Король",
    #     townhall_img="late_middle",
    #     buildings_img=["late_middle_brewery", "late_middle_foundry"],
    #     next_age_price=[13200, 8705],
    #     citizen=citizens.late_middle_citizen,
    #     home_building=homes.late_middle_home,
    #     food_building=buildings.late_middle_brewery,
    #     stock_building=buildings.late_middle_foundry,
    #     units=[units.halberdist, units.crossbowman, units.paladin],
    #     territories=[territories.muderia, territories.brovadia, territories.seligia, ]
    # )

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
