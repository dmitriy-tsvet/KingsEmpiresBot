import sqlite3
import json


async def db_execute(query):
    db = sqlite3.connect("database.db")
    sql = db.cursor()
    sql.execute(query)
    db.commit()
    sql.close()
    db.close()


def db_fetchone(query):
    db = sqlite3.connect("database.db")
    sql = db.cursor()
    sql.execute(query)
    fetch = sql.fetchone()
    sql.close()
    db.close()
    return fetch


async def db_fetchall(query):
    db = sqlite3.connect("database.db")
    sql = db.cursor()
    sql.execute(query)
    fetch = sql.fetchall()
    sql.close()
    db.close()
    return fetch


def get_townhall_table(user_id):
    result = db_fetchone(
        "SELECT * FROM townhall WHERE user_id = {};".format(user_id))

    if result is None:
        return None

    columns = ["id", "user_id", "user_mention",
               "country_name", "population",
               "age", "money", "money_timer",
               "food", "stock", "energy", "graviton",
               "territory_timer"
               ]
    data = {}
    for i in range(0, 13):
        if columns[i] in ("ability", "ability_reload", "items",
                          "kit", "skills", "health", "quest",
                          "achievements"):
            data.update({columns[i]: json.loads(result[i])})
            continue
        data.update({columns[i]: result[i]})

        if columns[i] not in ("work", "place") and result[i] is None:
            return None
    return data


async def get_buildings_table(user_id, type_resource):
    result = await db_fetchone(
        "SELECT * FROM {}_buildings WHERE user_id = {};".format(
            type_resource, user_id)
    )
    if result is None:
        return None

    columns = ["user_id", "count_buildings",
               "first_building", "first_building_lvl",
               "second_building", "second_building_lvl",
               "third_building", "third_building_lvl",
               "fourth_building", "fourth_building_lvl",
               "timer", "build_timer", "build_num"
               ]
    data = {}

    for i in range(0, 13):
        data.update({columns[i]: result[i]})

    return data


async def get_units_table(user_id):
    result = await db_fetchone(
        "SELECT * FROM units WHERE user_id = {};".format(user_id)
    )
    if result is None:
        return None

    columns = ["user_id", "units_count",
               "creation_queue", "creation_timer",
               "unit_1", "unit_1_lvl",
               "unit_2", "unit_2_lvl",
               "upgrade_timer", "upgrade_unit_num"
               ]
    data = {}

    for i in range(0, 10):
        data.update({columns[i]: result[i]})

    return data


def get_territory_table(user_id):
    result = db_fetchone(
        "SELECT * FROM territory WHERE user_id = '{}';".format(user_id)
    )
    if result is None:
        return None

    columns = ["user_id", "tax_timer", "capture_timer",
               "territory_names", "territory_taxes", "territory_owned",
               "territory_units", "captured_territory", "territory_state",
               "fight_state"
               ]
    data = {}

    for i in range(0, 10):
        if columns[i] in (
                "territory_names", "territory_taxes",
                "territory_owned", "territory_units"
        ):
            data.update({columns[i]: json.loads(result[i])})
            continue

        data.update({columns[i]: result[i]})

    return data


def update_table_data(user_id, data, table="townhall"):
    db = sqlite3.connect("database.db")
    sql = db.cursor()

    for i in list(data.items()):
        record_data = "{}='{}'".format(i[0], i[1])

        if i[1] is None:
            record_data = "{}=NULL".format(i[0], i[1])
        if i[1] is int:
            record_data = "{}={}".format(i[0], i[1])

        else:
            sql.execute(
                "UPDATE {} SET {}"
                " WHERE user_id='{}';".format(table, record_data, user_id))

    db.commit()
    sql.close()
    db.close()


async def update_json_column(user_id, column, data, table="townhall"):

    json_data = json.dumps(data, ensure_ascii=False)
    column_data = {}

    for i in list(data.items()):
        column_data.update({i[0]: i[1]})

    json_data = json.dumps(column_data, ensure_ascii=False)

    update_table_data(user_id, {column: json_data}, table)
