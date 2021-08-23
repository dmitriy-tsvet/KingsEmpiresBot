from enum import Enum
from utils.ages import models, buildings, units, homes, citizens, territories


class AgesList(Enum):
    stone_age: models.Age = models.Age(
        name="Каменный",
        rank="Вождь",
        img="stone",
        next_age_price=[500, ],
        citizen=citizens.stone_citizen,
        home_building=homes.stone_home,
        food_building=buildings.hut,
        units=[units.swordsman, units.archer],
        territories=[territories.devalon, territories.milon]
    )

    bronze_age = models.Age(
        name="Бронзовый",
        rank="Староста",
        img="bronze",
        next_age_price=[700, 250],
        citizen=citizens.stone_citizen,
        home_building=homes.bronze_home,
        food_building=buildings.paddock,
        stock_building=buildings.pottery,
        units=[units.berserk, units.thrower],
        territories=[territories.brathia, territories.cregido, territories.seligia]
    )

    iron_age = models.Age(
        name="Железный",
        rank="Сенатор",
        img="iron",
        next_age_price=[999999999999, ],
        citizen=citizens.stone_citizen,
        home_building=homes.iron_home,
        food_building=buildings.winery,
        stock_building=buildings.sawmill,
        units=[units.legionary, units.hoplite, units.rider],
        territories=[territories.muderia, territories.brovadia, territories.seligia, ]
    )

    @staticmethod
    def get_list_ages():
        list_of_ages = list(map(lambda age: age.value.name, AgesList))
        return list_of_ages

    # @staticmethod
    # def get_text_territories():
    #     text = ""
    #     for i in AgesList:
    #         i.value.name
    #
    #     list_of_ages = list(map(lambda age: age.value.name, AgesList))
    #     return list_of_ages

    @staticmethod
    def get_age_model(age):
        for i in AgesList:
            if i.value.name == age:
                return i.value
