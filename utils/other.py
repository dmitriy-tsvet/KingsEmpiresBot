from utils.dicts import unit_upgrade_price


async def upgrade_unit(price, food=0, stock=0, energy=0):
    if food < (price["food"]):
        return False
    if stock < (price["stock"] * 1):
        return False
    if energy < (price["energy"] * 1):
        return False
    else:
        return True



