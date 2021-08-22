import random
from utils.dicts import age_buildings
from utils.db_api.db_api2 import update_table_data, get_townhall_table


async def set_new_buildings(user_id):
    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]

    await update_table_data(
        user_id=user_id,
        data={
            "count_buildings": 1,
            "first_building": age_buildings[age]["food"],
            "first_building_lvl": 1,
            "second_building": None,
            "second_building_lvl": 0,
            "third_building": None,
            "third_building_lvl": 0,
            "fourth_building": None,
            "fourth_building_lvl": 0,
            "timer": 0,
            "build_timer": 0,
            "build_num": None
        },
        table="food_buildings"
    )

    await update_table_data(
        user_id=user_id,
        data={
            "count_buildings": 1,
            "first_building": age_buildings[age]["stock"],
            "first_building_lvl": 1,
            "second_building": None,
            "second_building_lvl": 0,
            "third_building": None,
            "third_building_lvl": 0,
            "fourth_building": None,
            "fourth_building_lvl": 0,
            "timer": 0,
            "build_timer": 0,
            "build_num": None
        },
        table="stock_buildings"
    )