from utils.ages import models

#
# Stone Age
#

# < 500 people
stone_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[2, ],
    create_time_sec=8
)

# < 1500
bronze_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[4, 2],
    create_time_sec=12
)

# < 3200
iron_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[8, 4],
    create_time_sec=32
)

# < 5400
early_middle_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[14, 7],
    create_time_sec=47
)


# < 7900
high_middle_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[21, 9],
    create_time_sec=56
)


# < 10700
late_middle_citizen = models.Citizen(
    name="👨🏼‍🌾",
    create_price=[32, 16],
    create_time_sec=60
)

