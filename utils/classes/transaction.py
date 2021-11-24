import copy
from utils.db_api import tables
from utils.misc.fill_in_list import fill_in_list


class Purchase:

    @staticmethod
    def buy(price: list, townhall: tables.TownHall) -> bool:

        price = fill_in_list(price)
        if townhall.money < price[0]:
            return False
        if townhall.stock < price[1]:
            return False
        if townhall.diamonds < price[2]:
            return False
        else:
            townhall.money -= price[0]
            townhall.stock -= price[1]
            townhall.diamonds -= price[2]
            return True

    @staticmethod
    def get_dynamic_price(price: list, townhall: tables.TownHall) -> str:
        text = ""
        emoji = ["💰", "⚒", "💎"]
        price = fill_in_list(price)

        price[0] -= townhall.money
        price[1] -= townhall.stock
        price[2] -= townhall.diamonds

        for i in price:
            if i < 0:
                price[price.index(i)] = 0

        for i in range(0, 2):
            if price[i] > 0:
                text += "{} {}".format(price[i], emoji[i])

                if price[-price.count(0)-1] != price[i]:
                    text += ", "

        return text

    @staticmethod
    def get_price(price: list) -> str:
        text = ""
        emoji = ["💰, ", "⚒", "💎"]

        price = fill_in_list(price)
        for i in range(0, 3):
            if price[i] != 0:

                text += "{} {}".format(price[i], emoji[i])

        return text

    @staticmethod
    def get_max_create_num(price: list, townhall: tables.TownHall) -> int:
        player_resources = [townhall.money, townhall.stock]
        max_nums = []

        for resource in player_resources:
            index = player_resources.index(resource)
            if resource == 0:
                create_max = 0
            else:
                create_max = int(resource / price[index])
            max_nums.append(create_max)
        if max_nums[0] > max_nums[1]:
            return max_nums[1]
        else:
            return max_nums[0]
