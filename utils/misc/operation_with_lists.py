

def subtract_nums_list(num: int, some_list: list) -> list:
    new_list = [i for i, x in enumerate(some_list)]
    empty_list = [0 for i in some_list]

    if new_list:
        while num > 0 and some_list != empty_list:
            for i in new_list:
                if some_list[i] <= 0:
                    continue

                if num <= 0:
                    break

                some_list[i] -= 1
                num -= 1

    return some_list


def add_nums_list(num: int, some_list: list) -> list:
    new_list = [i for i, x in enumerate(some_list)]

    if new_list:
        while num > 0:
            for i in new_list:
                if num <= 0:
                    break

                some_list[i] += 1
                num -= 1

    return some_list
