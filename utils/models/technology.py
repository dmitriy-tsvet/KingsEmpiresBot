from enum import Enum
from utils.models import base, home, stock_building, unit, manufacture_building
import typing

stone_home = base.Technology(
    name=home.stone_home.name,
    unlock_price=[0, 0],
    unlock_score=3,
    unlock_technology=home.stone_home
)

stone_hut = base.Technology(
    name=stock_building.stone_hut.name,
    unlock_price=[0, 0],
    unlock_score=3,
    unlock_technology=stock_building.stone_hut
)

stone_militia = base.Technology(
    name=unit.stone_militia.name,
    unlock_price=[0, 0],
    unlock_score=3,
    unlock_technology=unit.stone_militia
)


bronze_home_1 = base.Technology(
    name=home.bronze_home_1.name,
    unlock_price=[50, 50],
    unlock_score=4,
    unlock_technology=home.bronze_home_1
)

bronze_home_2 = base.Technology(
    name=home.bronze_home_2.name,
    unlock_price=[0, 0],
    unlock_score=4,
    unlock_technology=home.bronze_home_2
)

bronze_home_3 = base.Technology(
    name=home.bronze_home_3.name,
    unlock_price=[0, 0],
    unlock_score=1,
    unlock_technology=home.bronze_home_3
)


bronze_spearman = base.Technology(
    name=unit.bronze_swordsman.name,
    unlock_price=[50, 50],
    unlock_score=5,
    unlock_technology=unit.bronze_swordsman
)

bronze_archer = base.Technology(
    name=unit.bronze_archer.name,
    unlock_price=[50, 50],
    unlock_score=5,
    unlock_technology=unit.bronze_archer
)

bronze_sawmil = base.Technology(
    name=stock_building.bronze_sawmill.name,
    unlock_price=[50, 50],
    unlock_score=6,
    unlock_technology=stock_building.bronze_sawmill
)

bronze_forager = base.Technology(
    name=stock_building.bronze_forager.name,
    unlock_price=[0, 0],
    unlock_score=2,
    unlock_technology=stock_building.bronze_forager
)

bronze_winery = base.Technology(
    name=stock_building.bronze_winery.name,
    unlock_price=[50, 50],
    unlock_score=6,
    unlock_technology=stock_building.bronze_winery
)

bronze_pottery = base.Technology(
    name=manufacture_building.bronze_pottery.name,
    unlock_price=[50, 50],
    unlock_score=8,
    unlock_technology=manufacture_building.bronze_pottery
)

bronze_plantation = base.Technology(
    name=manufacture_building.bronze_plantation.name,
    unlock_price=[50, 50],
    unlock_score=8,
    unlock_technology=manufacture_building.bronze_plantation
)

iron_home = base.Technology(
    name=home.iron_home.name,
    unlock_price=[50, 50],
    unlock_score=3,
    unlock_technology=home.iron_home
)




