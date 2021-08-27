from utils.ages import models

#
# Stone Age
#

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
    create_price=[14, 7, ],
    create_time_sec=70,
    upgrade_price=[90, ],
    upgrade_time_sec=600,
    max_lvl=4,

)

hoplite = models.Unit(
    name="🗡 Гоплит",
    weight=3.2,
    create_price=[21, 5],
    create_time_sec=120,
    upgrade_price=[78, 20],
    upgrade_time_sec=780,
    max_lvl=6,
)

#
# Early Middle Age
#

archer = models.Unit(
    name="🏹 Лучник",
    weight=2.7,
    create_price=[14, 9, ],
    create_time_sec=70,
    upgrade_price=[90, ],
    upgrade_time_sec=600,
    max_lvl=4,

)

rider = models.Unit(
    name="🐴 Всадник",
    weight=3.2,
    create_price=[21, 5],
    create_time_sec=120,
    upgrade_price=[78, 20],
    upgrade_time_sec=780,
    max_lvl=6,
)


#
# High Middle Age
#

healer = models.Unit(
    name="📿 Лекарь",
    weight=6.0,
    create_price=[70, ],
    create_time_sec=150,
    upgrade_price=[48, 140],
    upgrade_time_sec=900,
    max_lvl=3,
)

mercenary = models.Unit(
    name="🪓 Наемник",
    weight=6.0,
    create_price=[70, ],
    create_time_sec=150,
    upgrade_price=[48, 140],
    upgrade_time_sec=900,
    max_lvl=3,
)

#
# Late Middle Age
#

halberdist = models.Unit(
    name="🗡 Алебардист",
    weight=6.0,
    create_price=[70, ],
    create_time_sec=150,
    upgrade_price=[48, 140],
    upgrade_time_sec=900,
    max_lvl=3,
)

crossbowman = models.Unit(
    name="🏹 Арбалетчик",
    weight=6.0,
    create_price=[70, ],
    create_time_sec=150,
    upgrade_price=[48, 140],
    upgrade_time_sec=900,
    max_lvl=3,
)

paladin = models.Unit(
    name="🐴🛡 Паладин",
    weight=6.0,
    create_price=[70, ],
    create_time_sec=150,
    upgrade_price=[48, 140],
    upgrade_time_sec=900,
    max_lvl=3,
)



