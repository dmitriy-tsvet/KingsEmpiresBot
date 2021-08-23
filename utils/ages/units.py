from utils.ages import models

#
# Stone Age
#

archer = models.Unit(
    name="🏹 Лучник",
    weight=1.2,
    create_price=[4, ],
    create_time_sec=12,
    upgrade_price=[20, ],
    upgrade_time_sec=360,
    max_lvl=6,
)

swordsman = models.Unit(
    name="🗡 Мечник",
    weight=1.8,
    create_price=[7, ],
    create_time_sec=18,
    upgrade_price=[40, ],
    upgrade_time_sec=480,
    max_lvl=4,
)

#
# Bronze Age
#

berserk = models.Unit(
    name="🪓 Берсерк",
    weight=3.4,
    create_price=[9, 2, ],
    create_time_sec=21,
    upgrade_price=[74, ],
    upgrade_time_sec=540,
    max_lvl=3,

)

thrower = models.Unit(
    name="🔪 Метатель",
    weight=1.9,
    create_price=[6, 4, ],
    create_time_sec=28,
    upgrade_price=[50, ],
    upgrade_time_sec=420,
    max_lvl=5,

)


#
# Iron Age
#

legionary = models.Unit(
    name="🛡 Легионер",
    weight=2.7,
    create_price=[60, 40,],
    create_time_sec=70,
    upgrade_price=[200, ],
    upgrade_time_sec=30,
    max_lvl=4,

)

hoplite = models.Unit(
    name="🗡 Гоплит",
    weight=6.0,
    create_price=[110, ],
    create_time_sec=220,
    upgrade_price=[200, ],
    upgrade_time_sec=30,
    max_lvl=6,
)


rider = models.Unit(
    name="🐴 Всадник",
    weight=6.0,
    create_price=[110, ],
    create_time_sec=220,
    upgrade_price=[200, ],
    upgrade_time_sec=30,
    max_lvl=6,
)



