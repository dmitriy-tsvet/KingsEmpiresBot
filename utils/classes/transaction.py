from utils.classes import other


class Transaction:

    @staticmethod
    def subtract_resources(price: list, townhall_table) -> bool:
        if townhall_table.food < price[0]:
            return False
        if townhall_table.stock < price[1]:
            return False
        else:
            townhall_table.food -= price[0]
            townhall_table.stock -= price[1]
            return True

    @staticmethod
    def get_text_price(price: list):
        text = ""
        emoji = list(other.ListEmojiResources)

        for i in range(0, 4):
            if price[i] != 0:
                text += "{} {}".format(price[i], emoji[i])

                if price[-price.count(0)-1] != price[i]:
                    text += ", "

        return text

    @staticmethod
    def get_max_create_num(price: list, townhall_table) -> int:
        try:
            if price[1] == 0:
                food_max_num = int(townhall_table.food / price[0])
                return food_max_num

            elif price[2] == 0:
                food_max_num = int(townhall_table.food / price[0])
                stock_max_num = int(townhall_table.stock / price[1])

                if food_max_num > stock_max_num:
                    return stock_max_num
                elif stock_max_num > food_max_num:
                    return food_max_num
                else:
                    return 0

        except ZeroDivisionError:
            return 0



