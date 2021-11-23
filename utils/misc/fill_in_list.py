
def fill_in_list(value: list):
    empty_list = [0 for i in range(0, 3 - len(value))]

    for i in empty_list:
        value.append(i)

    return value

