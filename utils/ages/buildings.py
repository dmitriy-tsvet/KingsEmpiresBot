from utils.ages import models

#
# Stone Age
#

hut = models.Building(
    name="🥓 Хибара Охотника",
    resource="food",
    efficiency=200,
    create_price=50,
    create_time_sec=300,
    upgrade_price=25,
    upgrade_time_sec=180,

)

#
# Bronze Age
#

paddock = models.Building(
    name="🐑 Загон",
    resource="food",
    efficiency=350,
    create_price=80,
    create_time_sec=30,
    upgrade_price=50,
    upgrade_time_sec=30,

)


pottery = models.Building(
    name="🏺 Гончарня",
    resource="stock",
    efficiency=100,
    create_price=65,
    create_time_sec=900,
    upgrade_price=30,
    upgrade_time_sec=660,

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




