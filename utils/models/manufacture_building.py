from utils.models import base, product

#
# Bronze Age
#

BronzePottery = base.ManufactureBuilding(
    name="🏺🏠 Гончарня",
    products=[product.dish, product.jug, product.amphora],
    create_price=[340, 490],
    create_time_sec=1800,
    manpower=108
)

BronzePlantation = base.ManufactureBuilding(
    name="🍇🏠 Плантация",
    products=[product.grape, product.pear, product.melon],
    create_price=[340, 490],
    create_time_sec=1800,
    manpower=108
)

# Iron Age

IronForger = base.ManufactureBuilding(
    name="🥩🏠 Мясник",
    products=[product.meat, product.chicken],
    create_price=[1500, 2400],
    create_time_sec=5400,
    manpower=230
)


IronButcher = base.ManufactureBuilding(
    name="🧵🏠 Портной",
    products=[product.threads, product.socks],
    create_price=[1500, 2400],
    create_time_sec=5400,
    manpower=230
)


