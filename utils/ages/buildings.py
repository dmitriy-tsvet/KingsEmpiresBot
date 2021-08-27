from utils.ages import models

#
# Stone Age
#

stone_hut = models.Building(
    name="🥓 Хибара Охотника",
    resource="food",
    efficiency=200,
    create_price=50,
    create_time_sec=1,
    upgrade_price=25,
    upgrade_time_sec=1,

)

#
# Bronze Age
#

bronze_winery = models.Building(
    name="🍷 Винодельня",
    resource="food",
    efficiency=350,
    create_price=220,
    create_time_sec=780,
    upgrade_price=45,
    upgrade_time_sec=360,

)


bronze_pottery = models.Building(
    name="🏺 Гончарня",
    resource="stock",
    efficiency=100,
    create_price=65,
    create_time_sec=900,
    upgrade_price=30,
    upgrade_time_sec=480,

)

#
# Iron Age
#

iron_butcher = models.Building(
    name="🥩 Мясник",
    resource="food",
    efficiency=800,
    create_price=705,
    create_time_sec=1560,
    upgrade_price=300,
    upgrade_time_sec=780,

)

iron_sawmill = models.Building(
    name="🪓 Лесопилка",
    resource="stock",
    efficiency=300,
    create_price=450,
    create_time_sec=1380,
    upgrade_price=310,
    upgrade_time_sec=660,

)


#
# Early Middle Age
#

early_middle_bakery = models.Building(
    name="🍞 Пекарня",
    resource="food",
    efficiency=1200,
    create_price=1050,
    create_time_sec=1800,
    upgrade_price=535,
    upgrade_time_sec=900,

)

early_middle_forge = models.Building(
    name="⚒ Кузнец",
    resource="stock",
    efficiency=500,
    create_price=730,
    create_time_sec=1560,
    upgrade_price=470,
    upgrade_time_sec=770,

)

#
# High Middle Age
#

high_middle_farm = models.Building(
    name="👩‍🌾 Ферма",
    resource="food",
    efficiency=1520,
    create_price=1450,
    create_time_sec=2100,
    upgrade_price=780,
    upgrade_time_sec=1020,

)

high_middle_herbalist = models.Building(
    name="🌿 Травник",
    resource="stock",
    efficiency=800,
    create_price=1070,
    create_time_sec=1740,
    upgrade_price=590,
    upgrade_time_sec=900,

)

#
# Late Middle Age
#

late_middle_brewery = models.Building(
    name="🍺 Пивоварня",
    resource="food",
    efficiency=2007,
    create_price=1850,
    create_time_sec=2520,
    upgrade_price=970,
    upgrade_time_sec=1380,

)

late_middle_foundry = models.Building(
    name="🗜 Литейная",
    resource="stock",
    efficiency=1365,
    create_price=1590,
    create_time_sec=2160,
    upgrade_price=820,
    upgrade_time_sec=1080,

)


