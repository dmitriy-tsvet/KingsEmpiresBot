from utils.models import base

#
# Stone Age
#

StoneMilitia = base.Unit(
    name="🪨 Ополченец",
    type_unit="Легкий юнит",
    damage=3,
    armor=3,
    create_price=[5, 5],
    create_time_sec=20,
)

#
# Bronze Age
#

BronzeSwordsman = base.Unit(
    name="🗡 Мечник",
    type_unit="Легкий юнит",
    damage=7,
    armor=7,
    create_price=[25, 25],
    create_time_sec=30,

)

BronzeArcher = base.Unit(
    name="🏹 Лучник",
    type_unit="Стрелок",
    damage=10,
    armor=4,
    create_price=[30, 5],
    create_time_sec=20,

)

#
# Iron Age
#

IronLegionary = base.Unit(
    name="🛡 Легионер",
    type_unit="Легкий воин",
    damage=9,
    armor=9,
    create_price=[100, 100],
    create_time_sec=40,
)

IronRider = base.Unit(
    name="🐴 Всадник",
    type_unit="Тяжелый воин",
    damage=8,
    armor=13,
    create_price=[230],
    create_time_sec=80,
)
