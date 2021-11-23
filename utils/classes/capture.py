import random
import time
from utils.classes import maths


class Capture:
    def __init__(self, army_1: int, army_2: int):
        self.army_1 = army_1
        self.army_2 = army_2

    def is_win(self) -> bool:
        data = {}

        if self.army_1 > self.army_2:
            large_army = self.army_1
            small_army = self.army_2

            data.update({
                "large": True,
                "small": False,
            })

        elif self.army_1 < self.army_2:
            large_army = self.army_2
            small_army = self.army_1

            data.update({
                "large": False,
                "small": True,
            })

        else:
            random_num = random.choice([0, 1])
            if random_num == 1:
                return False
            else:
                return True

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
                return False
            else:
                return True

    def scouting(self) -> int:
        data = {}

        if self.army_1 > self.army_2:
            large_army = self.army_1
            small_army = self.army_2

            data.update({
                "large": True,
                "small": False,
            })

        elif self.army_1 < self.army_2:
            large_army = self.army_2
            small_army = self.army_1

            data.update({
                "large": False,
                "small": True,
            })

        else:
            return 50

        large_army_80 = maths.Maths.subtract_percent(large_army, 80)
        large_army_60 = maths.Maths.subtract_percent(large_army, 60)
        large_army_40 = maths.Maths.subtract_percent(large_army, 40)
        large_army_20 = maths.Maths.subtract_percent(large_army, 20)
        large_army_10 = maths.Maths.subtract_percent(large_army, 10)

        if large_army_80 > small_army:
            if data["large"]:
                return 100
            else:
                return 0

        elif large_army_60 > small_army:
            if data["large"]:
                return 95
            else:
                return 5

        elif large_army_40 > small_army:
            if data["large"]:
                return 80
            else:
                return 20

        elif large_army_20 > small_army:
            if data["large"]:
                return 70
            else:
                return 30
        elif large_army_10 > small_army:
            if data["large"]:
                return 60
            else:
                return 40
        else:
            if data["large"]:
                return 50
            else:
                return 50
