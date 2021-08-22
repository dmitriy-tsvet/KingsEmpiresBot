from utils.ages import models

#
# Stone Age
#

archer = models.Unit(
    name="🏹 Лучник",
    weight=1.2,
    create_price=[10, ],
    create_time_sec=4,
    upgrade_price=[200, ],
    upgrade_time_sec=5,
    max_lvl=6,
)

swordsman = models.Unit(
    name="🗡 Мечник",
    weight=1.8,
    create_price=[25, ],
    create_time_sec=5,
    upgrade_price=[200, ],
    upgrade_time_sec=30,
    max_lvl=4,
)

#
# Bronze Age
#

berserk = models.Unit(
    name="🪓 Берсерк",
    weight=3.4,
    create_price=[60, 10,],
    create_time_sec=90,
    upgrade_price=[200, ],
    upgrade_time_sec=5,
    max_lvl=3,

)

thrower = models.Unit(
    name="🔪 Метатель",
    weight=1.9,
    create_price=[40, 20, ],
    create_time_sec=70,
    upgrade_price=[200, ],
    upgrade_time_sec=5,
    max_lvl=5,

)

shaman = models.Unit(
    name="📿 Шаман",
    weight=1.9,
    create_price=[40, 20,],
    create_time_sec=70,
    upgrade_price=[200, ],
    upgrade_time_sec=5,
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



