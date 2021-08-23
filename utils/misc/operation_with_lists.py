import random


def subtract_nums_list(num: int, some_list: list) -> list:
    new_list = [i for i, x in enumerate(some_list)]
    remainder = 0

    if new_list:
        while num > 0:
            for i in new_list:
                random_num = random.randint(0, num)
                some_list[i] -= random_num
                some_list[i] -= remainder
                num -= random_num

                if some_list[i] < 0:
                    remainder = some_list[i]
                    some_list[i] = 0

    return some_list


def add_nums_list(num: int, some_list: list) -> list:
    new_list = [i for i, x in enumerate(some_list)]

    if new_list:
        while num > 0:
            for i in new_list:
                random_num = random.randint(0, num)
                some_list[i] += random_num
                num -= random_num

    return some_list

