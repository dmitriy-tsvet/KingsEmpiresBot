from utils.dicts import age_resource_buff


def resource_lvl_buff(lvl):
    if lvl == 0:
        return 0
    lvl_buff = "1.{}".format(lvl)
    lvl_buff = float(lvl_buff) - 0.1
    lvl_buff += 0.001
    return lvl_buff
