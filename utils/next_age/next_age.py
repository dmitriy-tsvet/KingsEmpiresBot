from utils.next_age.set_new_territory import set_new_territory
from utils.next_age.set_new_buildings import set_new_buildings
from utils.next_age.set_new_units import set_new_units


async def next_age_func(user_id):
    await set_new_territory(user_id)
    await set_new_buildings(user_id)
    await set_new_units(user_id)
