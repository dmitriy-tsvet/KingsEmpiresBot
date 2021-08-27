from utils.ages import models

#
# Stone Age
#

stone_home = models.HomeBuilding(
    name="⛺",
    img="stone",
    capacity=15,
    create_price=10,
    create_time_sec=120

)


bronze_home = models.HomeBuilding(
    name="🏠",
    img="bronze",
    capacity=30,
    create_price=50,
    create_time_sec=240

)

iron_home = models.HomeBuilding(
    name="🏠",
    img="iron",
    capacity=48,
    create_price=100,
    create_time_sec=600
)

early_middle_home = models.HomeBuilding(
    name="🏡",
    img="early_middle",
    capacity=61,
    create_price=225,
    create_time_sec=780
)


high_middle_home = models.HomeBuilding(
    name="🏡",
    img="high_middle",
    capacity=73,
    create_price=290,
    create_time_sec=900
)


late_middle_home = models.HomeBuilding(
    name="🏡",
    img="late_middle",
    capacity=78,
    create_price=470,
    create_time_sec=1200
)

