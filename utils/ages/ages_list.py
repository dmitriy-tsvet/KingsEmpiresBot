from enum import Enum
from utils.ages import models, buildings, units, homes, citizens, territories


class AgesList(Enum):
    stone_age: models.Age = models.Age(
        name="Каменный",
        rank="Вождь",
        townhall_img="stone",
        buildings_img=["stone_hut"],
        next_age_price=[1120, ],
        citizen=citizens.stone_citizen,
        home_building=homes.stone_home,
        food_building=buildings.stone_hut,
        units=[units.swordsman],
        territories=[territories.devalon, territories.milon]
    )

    bronze_age = models.Age(
        name="Бронзовый",
        rank="Староста",
        townhall_img="bronze",
        buildings_img=["bronze_winery", "bronze_pottery"],
        next_age_price=[2105, 560],
        citizen=citizens.bronze_citizen,
        home_building=homes.bronze_home,
        food_building=buildings.bronze_winery,
        stock_building=buildings.bronze_pottery,
        units=[units.berserk, units.thrower],
        territories=[territories.brathia, territories.cregido, territories.seligia]
    )

    iron_age = models.Age(
        name="Железный",
        rank="Сенатор",
        townhall_img="iron",
        buildings_img=["iron_butcher", "iron_sawmill"],
        next_age_price=[4680, 1800],
        citizen=citizens.iron_citizen,
        home_building=homes.iron_home,
        food_building=buildings.iron_butcher,
        stock_building=buildings.iron_sawmill,
        units=[units.legionary, units.hoplite],
        territories=[territories.muderia, territories.brovadia, territories.hitopia, ]
    )

    early_middle_age = models.Age(
        name="Раннее Средневековье",
        rank="Барон",
        townhall_img="early_middle",
        buildings_img=["early_middle_bakery", "early_middle_forge"],
        next_age_price=[7205, 2700],
        citizen=citizens.early_middle_citizen,
        home_building=homes.early_middle_home,
        food_building=buildings.early_middle_bakery,
        stock_building=buildings.early_middle_forge,
        units=[units.archer, units.rider],
        territories=[territories.muderia, territories.brovadia, territories.hitopia,  ]
    )

    high_middle_age = models.Age(
        name="Высокое Средневековье",
        rank="Граф",
        townhall_img="high_middle",
        buildings_img=["high_middle_farm", "high_middle_herbalist"],
        next_age_price=[9105, 4480],
        citizen=citizens.high_middle_citizen,
        home_building=homes.high_middle_home,
        food_building=buildings.high_middle_farm,
        stock_building=buildings.high_middle_herbalist,
        units=[units.healer, units.mercenary],
        territories=[territories.muderia, territories.brovadia, territories.seligia, ]
    )

    late_middle_age = models.Age(
        name="Позднее Средневековье",
        rank="Король",
        townhall_img="late_middle",
        buildings_img=["late_middle_brewery", "late_middle_foundry"],
        next_age_price=[13200, 8705],
        citizen=citizens.late_middle_citizen,
        home_building=homes.late_middle_home,
        food_building=buildings.late_middle_brewery,
        stock_building=buildings.late_middle_foundry,
        units=[units.halberdist, units.crossbowman, units.paladin],
        territories=[territories.muderia, territories.brovadia, territories.seligia, ]
    )

    @staticmethod
    def get_list_ages():
        list_of_ages = list(map(lambda age: age.value.name, AgesList))
        return list_of_ages

    @staticmethod
    def get_age_model(age):
        for i in AgesList:
            if i.value.name == age:
                return i.value
