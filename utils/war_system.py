import random
import time
from utils.classes import maths


def fight(attack_army, defend_army):

    data = {}

    if attack_army > defend_army:
        large_army = attack_army
        small_army = defend_army

        data.update({
            "large": "attacker",
            "small": "defender",
        })

    elif attack_army < defend_army:
        large_army = defend_army
        small_army = attack_army

        data.update({
            "large": "defender",
            "small": "attacker",
        })

    else:
        random_num = random.choice([0, 1])
        if random_num == 1:
            return "defender"
        else:
            return "attacker"

    large_army_80 = maths.Maths.subtract_percent(large_army, 80)
    large_army_60 = maths.Maths.subtract_percent(large_army, 60)
    large_army_40 = maths.Maths.subtract_percent(large_army, 40)
    large_army_20 = maths.Maths.subtract_percent(large_army, 20)
    large_army_10 = maths.Maths.subtract_percent(large_army, 10)

    if large_army_80 > small_army:
        return data["large"]

    elif large_army_60 > small_army:
        random_num = random.choices([0, 1], [95, 5])[0]

        if random_num == 1:
            return data["small"]
        else:
            return data["large"]

    elif large_army_40 > small_army:
        random_num = random.choices([0, 1], [80, 20])[0]
        if random_num == 1:
            return data["small"]
        else:
            return data["large"]
    elif large_army_20 > small_army:
        random_num = random.choices([0, 1], [70, 30])[0]
        if random_num == 1:
            return data["small"]
        else:
            return data["large"]
    elif large_army_10 > small_army:
        random_num = random.choices([0, 1], [60, 40])[0]
        if random_num == 1:
            return data["small"]
        else:
            return data["large"]
    else:
        random_num = random.choice([0, 1])
        if random_num == 1:
            return "defender"
        else:
            return "attacker"


def riot(territory_owned, territory_units):
    owned = []

    for i in territory_owned:
        if i is not None:
            owned.append(i)

    if owned:
        riot_territory = random.choice(owned)
        index = territory_owned.index(riot_territory)
        random_percent = random.randint(30, 60)
        units = maths.Maths.subtract_percent(territory_units[index], random_percent)
        return {"units": units, "riot_territory": riot_territory}
    else:
        return None
