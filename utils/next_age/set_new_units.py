import random
from utils.dicts import age_units
from utils.db_api.db_api2 import update_table_data, get_townhall_table


async def set_new_units(user_id):
    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]
    await update_table_data(
        user_id=user_id,
        data={
            "unit_1": age_units[age]["unit_1"],
            "unit_1_lvl": 1,
            "unit_2": age_units[age]["unit_2"],
            "unit_2_lvl": 1,
            "upgrade_timer": 0,
            "upgrade_unit_num": None
        },
        table="units"
    )
