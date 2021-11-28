from utils.models import base

#
# Stone Age
#

stone_home = base.HomeBuilding(
    name="🛖 Хижина",
    capacity=14,
    income=72,
    create_price=[0, 60],
    create_time_sec=5

)

bronze_home_1 = base.HomeBuilding(
    name="⛺ Шале",
    capacity=30,
    income=8,
    create_price=[50],
    create_time_sec=240

)

bronze_home_2 = base.HomeBuilding(
    name="🛖🌳 Свайное жилище",
    capacity=22,
    income=44,
    create_price=[40, 140],
    create_time_sec=240

)

bronze_home_3 = base.HomeBuilding(
    name="⛺🐲 Дом Старейшины",
    capacity=70,
    income=100,
    create_price=[0, 0, 100],
    create_time_sec=5

)

# Iron Age

iron_home_1 = base.HomeBuilding(
    name="🏠☕ Коттедж",
    capacity=73,
    income=28,
    create_price=[250, 890],
    create_time_sec=1800
)

iron_home_2 = base.HomeBuilding(
    name="🏠🧱 Дом с Черепицей",
    capacity=44,
    income=60,
    create_price=[400, 600],
    create_time_sec=1200
)

iron_home_3 = base.HomeBuilding(
    name="🏠🌴 Вилла",
    capacity=87,
    income=100,
    create_price=[0, 0, 200],
    create_time_sec=20
)





