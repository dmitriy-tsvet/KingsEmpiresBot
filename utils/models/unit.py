from utils.models import base

#
# Stone Age
#

stone_militia = base.Unit(
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

bronze_swordsman = base.Unit(
    name="🗡 Мечник",
    type_unit="Легкий юнит",
    damage=7,
    armor=7,
    create_price=[25, 25],
    create_time_sec=30,

)

bronze_archer = base.Unit(
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

iron_legionary = base.Unit(
    name="🛡 Легионер",
    type_unit="Легкий воин",
    damage=9,
    armor=9,
    create_price=[100, 100],
    create_time_sec=40,
)

iron_rider = base.Unit(
    name="🐴 Всадник",
    type_unit="Тяжелый воин",
    damage=8,
    armor=13,
    create_price=[230],
    create_time_sec=80,
)

#
# Early Middle Age
#

# archer = models.Unit(
#     name="🏹 Лучник",
#     weight=2.7,
#     create_price=[14, 9, ],
#     create_time_sec=70,
#     upgrade_price=[90, ],
#     upgrade_time_sec=600,
#     max_lvl=4,
#
# )
#
# rider = models.Unit(
#     name="🐴 Всадник",
#     weight=3.2,
#     create_price=[21, 5],
#     create_time_sec=120,
#     upgrade_price=[78, 20],
#     upgrade_time_sec=780,
#     max_lvl=6,
# )
#
#
# #
# # High Middle Age
# #
#
# healer = models.Unit(
#     name="📿 Лекарь",
#     weight=6.0,
#     create_price=[70, ],
#     create_time_sec=150,
#     upgrade_price=[48, 140],
#     upgrade_time_sec=900,
#     max_lvl=3,
# )
#
# mercenary = models.Unit(
#     name="🪓 Наемник",
#     weight=6.0,
#     create_price=[70, ],
#     create_time_sec=150,
#     upgrade_price=[48, 140],
#     upgrade_time_sec=900,
#     max_lvl=3,
# )
#
# #
# # Late Middle Age
# #
#
# halberdist = models.Unit(
#     name="🗡 Алебардист",
#     weight=6.0,
#     create_price=[70, ],
#     create_time_sec=150,
#     upgrade_price=[48, 140],
#     upgrade_time_sec=900,
#     max_lvl=3,
# )
#
# crossbowman = models.Unit(
#     name="🏹 Арбалетчик",
#     weight=6.0,
#     create_price=[70, ],
#     create_time_sec=150,
#     upgrade_price=[48, 140],
#     upgrade_time_sec=900,
#     max_lvl=3,
# )
#
# paladin = models.Unit(
#     name="🐴🛡 Паладин",
#     weight=6.0,
#     create_price=[70, ],
#     create_time_sec=150,
#     upgrade_price=[48, 140],
#     upgrade_time_sec=900,
#     max_lvl=3,
# )
#
#
#
