from utils.ages import models

#
# Stone Age
#

hut = models.Building(
    name="🥓 Хибара Охотника",
    resource="food",
    efficiency=600,
    create_price=1000,
    create_time_sec=30,
    upgrade_price=500,
    upgrade_time_sec=40,

)

#
# Bronze Age
#

paddock = models.Building(
    name="🐑 Загон",
    resource="food",
    efficiency=800,
    create_price=2000,
    create_time_sec=30,
    upgrade_price=500,
    upgrade_time_sec=30,

)


pottery = models.Building(
    name="🏺 Гончарня",
    resource="stock",
    efficiency=600,
    create_price=2000,
    create_time_sec=30,
    upgrade_price=500,
    upgrade_time_sec=30,

)

#
# Iron Age
#

winery = models.Building(
    name="🍷 Винодельня",
    resource="food",
    efficiency=800,
    create_price=4500,
    create_time_sec=70,
    upgrade_price=500,
    upgrade_time_sec=30,

)

sawmill = models.Building(
    name="🪓 Лесопилка",
    resource="stock",
    efficiency=500,
    create_price=3000,
    create_time_sec=30,
    upgrade_price=500,
    upgrade_time_sec=30,

)




