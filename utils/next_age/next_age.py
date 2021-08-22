from utils.next_age.set_new_territory import set_new_territory
from utils.next_age.set_new_buildings import set_new_buildings
from utils.next_age.set_new_units import set_new_units


async def next_age_func(callback):
    user_id = callback.from_user.id

    await set_new_territory(user_id)
    await set_new_buildings(user_id)
    await set_new_units(user_id)
    await callback.answer("")
    await callback.message.answer("✨")
    await callback.message.answer(
        "Поздравляю {}, ты переходишь в новый век.".format(
            callback.from_user.get_mention()
        )
    )
