from utils.db_api.db_api2 import update_table_data, get_townhall_table
import random


async def population_growth(user_id):
    townhall_data = get_townhall_table(user_id)
    population = townhall_data["population"]

    num = random.choices([0, 1], [70, 30])[0]

    if num == 1:
        people = random.randint(5, 20)
        population += people
        await update_table_data(
            user_id=user_id,
            data={
                "population": population
            }
        )
