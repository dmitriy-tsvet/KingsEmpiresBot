from utils.models import base

#
# Stone Age
#

StoneHut = base.StockBuilding(
    name="🥓🏠 Хибара Охотника",
    efficiency=78,
    create_price=[96, ],
    create_time_sec=5,
    manpower=28
)

#
# Bronze Age
#

BronzeSawmill = base.StockBuilding(
    name="🪓🏠 Лесопилка",
    efficiency=62,
    create_price=[430, 40],
    create_time_sec=1200,
    manpower=12
)

BronzeForager = base.StockBuilding(
    name="⛓🏠 Кузнец",
    efficiency=420,
    create_price=[0, 0, 200],
    create_time_sec=20,
    manpower=40
)


BronzeWinery = base.StockBuilding(
    name="🍷🏠 Винодельня",
    efficiency=97,
    create_price=[240, 30],
    create_time_sec=40,
    manpower=41
)

#
# Iron Age
#

IronFoundry = base.StockBuilding(
    name="▫🏠 Литейная железа",
    efficiency=360,
    create_price=[4100, 410],
    create_time_sec=4200,
    manpower=66
)

IronJewelry = base.StockBuilding(
    name="💍🏠 Ювелирная",
    efficiency=480,
    create_price=[4800, 680],
    create_time_sec=6000,
    manpower=122
)

IronFelting = base.StockBuilding(
    name="🧶🏠 Сукновальня",
    efficiency=720,
    create_price=[0, 0, 400],
    create_time_sec=20,
    manpower=88
)