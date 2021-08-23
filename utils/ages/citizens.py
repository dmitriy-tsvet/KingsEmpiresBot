from utils.ages import models

#
# Stone Age
#

stone_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[2, ],
    create_time_sec=8
)

bronze_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[4, 2],
    create_time_sec=12
)

iron_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[8, 4],
    create_time_sec=12
)
