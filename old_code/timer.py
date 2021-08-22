import time
import json

from utils.db_api.db_api2 import get_townhall_table,\
    update_table_data, get_buildings_table, get_territory_table, get_units_table
from utils.dicts import age_lvl, age_resource_buff, units_create_timer, age_units
from utils.resource_lvl_buff import resource_lvl_buff


async def people_growth_time():
    pass


async def set_money_timer(user_id):
    townhall_table = await get_townhall_table(user_id)
    population = townhall_table["population"]

    money_people = int(population * 2)
    time_set = int(time.time() + 3600)

    money_min = int(money_people / 60)

    return time_set


async def get_money_timer(user_id):
    townhall_table = await get_townhall_table(user_id)
    population = townhall_table["population"]
    age = townhall_table["age"]

    timer = int(townhall_table["money_timer"])
    time_left_sec = int(timer - time.time())
    time_left_min = int((time_left_sec / 60))

    if time_left_min < 0:
        time_left_min = 0

    money_people = int(population * 2)
    money_min = int(money_people / 60)

    time_passed = 60 - time_left_min

    if time_left_min >= 59:
        money = 0
    else:
        money = int(time_passed * money_min) * age_lvl[age]

    await set_money_timer(user_id)
    return money


async def set_resource_timer(user_id, type_resource):
    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]

    time_set = int(time.time() + 3600)

    resource_buff = age_resource_buff[age][type_resource]

    resource_min = int(resource_buff / 60)

    await update_table_data(
        user_id=user_id,
        data={"timer": time_set},
        table="{}_buildings".format(type_resource))

    return resource_min


async def get_resource_timer(user_id, type_resource):
    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]
    buildings_table = await get_buildings_table(user_id, type_resource)
    count_buildings = buildings_table["count_buildings"]

    resource_buff = age_resource_buff[age][type_resource]

    first_building = await resource_lvl_buff(
        lvl=buildings_table["first_building_lvl"]
    )
    second_building = await resource_lvl_buff(
        lvl=buildings_table["second_building_lvl"]
    )
    third_building = await resource_lvl_buff(
        lvl=buildings_table["third_building_lvl"]
    )
    fourth_building = await resource_lvl_buff(
        lvl=buildings_table["fourth_building_lvl"]
    )

    buildings = [first_building, second_building, third_building, fourth_building]
    buildings_lvl = sum(buildings) - 0.1

    timer = int(buildings_table["timer"])
    time_left_sec = int(timer - time.time())
    time_left_min = int((time_left_sec / 60))

    if time_left_min <= 0:
        time_left_min = 0

    resource_min = resource_buff / 60
    time_passed_min = 60 - time_left_min

    if time_left_min >= 59:
        resource_buff = 0
    else:
        resource_buff = (time_passed_min * resource_min) * buildings_lvl

    resource_buff = int(resource_buff)
    await set_resource_timer(user_id, type_resource)
    return resource_buff


async def set_build_timer(user_id, type_resource, num_building):
    time_set = int(time.time() + 720)
    time_left_sec = int(time_set - time.time())
    time_left_min = int(time_left_sec / 60)
    time_left_hour = int(time_left_min / 60)

    await update_table_data(
        user_id=user_id,
        data={
            "build_timer": time_set,
            "build_num": num_building
        },
        table="{}_buildings".format(type_resource))

    return time_left_min + 1


async def get_build_timer(timer, ):
    time_left_sec = int(timer - time.time())
    time_left_min = int(time_left_sec / 60)
    time_left_hour = int(time_left_min / 60)

    if time_left_min > 59:
        data = {
            "time": time_left_hour,
            "measure": "ч."
            }
        return data

    else:
        data = {
            "time": time_left_min,
            "measure": "мин."
        }

        return data


async def set_capture_timer(user_id):
    time_set = int(time.time() + 1260)
    time_left_sec = int(time_set - time.time())
    time_left_min = int(time_left_sec / 60)
    time_left_hour = int(time_left_min / 60)

    await update_table_data(
        user_id=user_id,
        data={
            "capture_timer": time_set,
        },
        table="territory")

    return time_left_min


async def get_time_left(timer):

    if timer <= 0:
        timer = 0
        return timer

    time_left_sec = int(timer - time.time())
    time_left_min = int(time_left_sec / 60)
    time_left_hour = int(time_left_min / 60)

    return time_left_min


async def set_tax_timer(user_id):
    territory_table = await get_territory_table(user_id)
    territory_owned = territory_table["territory_owned"]
    territory_taxes = territory_table["territory_taxes"]
    tax = 0

    for i in territory_owned:
        if i is not None:
            index = territory_owned.index(i)
            tax += territory_taxes[index]

    time_set = int(time.time() + 3600)
    time_left_sec = time_set - time.time()
    time_left_min = int((time_left_sec / 60))

    tax = int(tax / 60)

    await update_table_data(
        user_id=user_id,
        data={"tax_timer": time_set},
        table="territory"
    )
    return tax


async def get_tax_timer(user_id):
    territory_table = await get_territory_table(user_id)
    territory_owned = territory_table["territory_owned"]
    territory_taxes = territory_table["territory_taxes"]
    tax = 0

    for i in territory_owned:
        if i is not None:
            index = territory_owned.index(i)

            tax += territory_taxes[index]

    timer = int(territory_table["tax_timer"])
    time_left_sec = int(timer - time.time())
    time_left_min = int((time_left_sec / 60))

    if time_left_min < 0:
        time_left_min = 0

    tax_min = int(tax / 60)

    time_passed = 60 - time_left_min

    if time_left_min >= 59:
        money = 0
    else:
        money = int(time_passed * tax_min)

    await set_tax_timer(user_id)
    return money


async def set_create_unit_timer(user_id, unit_num, units_count=1):
    townhall_table = await get_townhall_table(user_id)
    age = townhall_table["age"]

    units_table = await get_units_table(user_id)
    timer_create = float(units_table["creation_timer"] - time.time())
    if timer_create != 0:
        timer_create = float(units_table["creation_timer"] - time.time())

    if timer_create < 0:
        timer_create = 0

    time_in_sec = units_create_timer[age][unit_num] * units_count

    time_set = float(time.time() + time_in_sec + timer_create)
    time_left_sec = float(time_set - time.time())
    time_left_min = int(time_left_sec / 60)
    time_left_hour = int(time_left_min / 60)

    await update_table_data(
        user_id=user_id,
        data={
            "creation_timer".format(unit_num): time_set,
        },
        table="units")

    return time_left_min


async def set_upgrade_unit_timer(user_id, unit_num):
    time_set = int(time.time() + 1080)
    time_left_sec = int(time_set - time.time())
    time_left_min = int(time_left_sec / 60)
    time_left_hour = int(time_left_min / 60)

    await update_table_data(
        user_id=user_id,
        data={
            "upgrade_timer": time_set,
            "upgrade_unit_num": unit_num
        },
        table="units"
    )

    return time_left_min

