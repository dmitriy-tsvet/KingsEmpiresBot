from utils.models import base, product

#
# Bronze Age
#

bronze_pottery = base.ManufactureBuilding(
    name="🏺🏠 Гончарня",
    products=[product.dish, product.jug, product.amphora],
    create_price=[340, 490],
    create_time_sec=1800,
    manpower=108
)

bronze_plantation = base.ManufactureBuilding(
    name="🍇🏠 Плантация",
    products=[product.grape, product.pear, product.melon],
    create_price=[340, 490],
    create_time_sec=1800,
    manpower=108
)

#
# Iron Age
#

# bronze_pottery = base.ManufactureBuilding(
#     name="🧵 Портной",
#     products=[],
#     create_price=[96, ],
#     create_time_sec=20,
#
# )
#
# bronze_forger = base.ManufactureBuilding(
#     name="🔨 Мясник",
#     products=[],
#     create_price=[96, ],
#     create_time_sec=20,
#
# )
#

