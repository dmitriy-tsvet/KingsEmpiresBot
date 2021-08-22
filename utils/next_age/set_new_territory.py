import random, json
from utils.dicts import names_all_territories
from utils.db_api.db_api2 import update_table_data


async def set_new_territory(user_id):
    territory_names = names_all_territories
    random.shuffle(territory_names)
    territory_names = territory_names[:6]

    territory_taxes = [
        random.randint(200, 700),
        random.randint(500, 1500),
        random.randint(1000, 2500),
        random.randint(1500, 4000),
        random.randint(3000, 5000),
        random.randint(4000, 6000),
    ]
    territory_owned = [None for i in range(0, 6)]

    territory_units = [
        random.randint(100, 400),
        random.randint(300, 600),
        random.randint(800, 1200),
        random.randint(900, 1500),
        random.randint(1000, 1700),
        random.randint(1500, 2000),
    ]
    territory_names = json.dumps(territory_names, ensure_ascii=False)
    territory_taxes = json.dumps(territory_taxes, ensure_ascii=False)
    territory_owned = json.dumps(territory_owned, ensure_ascii=False)
    territory_units = json.dumps(territory_units, ensure_ascii=False)

    await update_table_data(
        user_id=user_id,
        data={
            "territory_names": territory_names,
            "territory_taxes": territory_taxes,
            "territory_owned": territory_owned,
            "territory_units": territory_units
        },
        table="territory"
    )
