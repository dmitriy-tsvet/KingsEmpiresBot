from enum import Enum
from utils.models import base, home, stock_building, unit, manufacture_building
import typing

StoneHome = base.Technology(
    name=home.StoneHome.name,
    unlock_price=[0, 0],
    unlock_score=3,
    unlock_technology=home.StoneHome
)

StoneHut = base.Technology(
    name=stock_building.StoneHut.name,
    unlock_price=[0, 0],
    unlock_score=3,
    unlock_technology=stock_building.StoneHut
)

StoneMilitia = base.Technology(
    name=unit.StoneMilitia.name,
    unlock_price=[0, 0],
    unlock_score=3,
    unlock_technology=unit.StoneMilitia
)


BronzeHome_1 = base.Technology(
    name=home.BronzeHome_1.name,
    unlock_price=[50, 50],
    unlock_score=4,
    unlock_technology=home.BronzeHome_1
)

BronzeHome_2 = base.Technology(
    name=home.BronzeHome_2.name,
    unlock_price=[0, 0],
    unlock_score=4,
    unlock_technology=home.BronzeHome_2
)

BronzeHome_3 = base.Technology(
    name=home.BronzeHome_3.name,
    unlock_price=[0, 0],
    unlock_score=1,
    unlock_technology=home.BronzeHome_3
)


BronzeSwordsman = base.Technology(
    name=unit.BronzeSwordsman.name,
    unlock_price=[50, 50],
    unlock_score=5,
    unlock_technology=unit.BronzeSwordsman
)

BronzeArcher = base.Technology(
    name=unit.BronzeArcher.name,
    unlock_price=[50, 50],
    unlock_score=5,
    unlock_technology=unit.BronzeArcher
)

BronzeSawmill = base.Technology(
    name=stock_building.BronzeSawmill.name,
    unlock_price=[50, 50],
    unlock_score=6,
    unlock_technology=stock_building.BronzeSawmill
)

BronzeForager = base.Technology(
    name=stock_building.BronzeForager.name,
    unlock_price=[0, 0],
    unlock_score=2,
    unlock_technology=stock_building.BronzeForager
)

BronzeWinery = base.Technology(
    name=stock_building.BronzeWinery.name,
    unlock_price=[50, 50],
    unlock_score=6,
    unlock_technology=stock_building.BronzeWinery
)

BronzePottery = base.Technology(
    name=manufacture_building.BronzePottery.name,
    unlock_price=[50, 50],
    unlock_score=8,
    unlock_technology=manufacture_building.BronzePottery
)

BronzePlantation = base.Technology(
    name=manufacture_building.BronzePlantation.name,
    unlock_price=[50, 50],
    unlock_score=8,
    unlock_technology=manufacture_building.BronzePlantation
)

IronHome_1 = base.Technology(
    name=home.IronHome_1.name,
    unlock_price=[250, 100],
    unlock_score=13,
    unlock_technology=home.IronHome_1
)

IronHome_2 = base.Technology(
    name=home.IronHome_2.name,
    unlock_price=[600, 1250],
    unlock_score=13,
    unlock_technology=home.IronHome_2
)

IronHome_3 = base.Technology(
    name=home.IronHome_3.name,
    unlock_price=[50, 50],
    unlock_score=4,
    unlock_technology=home.IronHome_3
)

IronLegionary = base.Technology(
    name=unit.IronLegionary.name,
    unlock_price=[0, 0],
    unlock_score=14,
    unlock_technology=unit.IronLegionary
)


IronRider = base.Technology(
    name=unit.IronRider.name,
    unlock_price=[1500, 2000],
    unlock_score=22,
    unlock_technology=unit.IronRider
)

IronFoundry = base.Technology(
    name=stock_building.IronFoundry.name,
    unlock_price=[0, 1500],
    unlock_score=11,
    unlock_technology=stock_building.IronFoundry
)

IronJewelry = base.Technology(
    name=stock_building.IronJewelry.name,
    unlock_price=[1500, 0],
    unlock_score=13,
    unlock_technology=stock_building.IronJewelry
)

IronFelting = base.Technology(
    name=stock_building.IronJewelry.name,
    unlock_price=[500, 0],
    unlock_score=6,
    unlock_technology=stock_building.IronFelting
)

IronForger = base.Technology(
    name=manufacture_building.IronForger.name,
    unlock_price=[300, 250],
    unlock_score=12,
    unlock_technology=manufacture_building.IronForger
)

IronButcher = base.Technology(
    name=manufacture_building.IronButcher.name,
    unlock_price=[100, 2500],
    unlock_score=16,
    unlock_technology=manufacture_building.IronButcher
)



