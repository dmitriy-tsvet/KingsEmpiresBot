from utils.models import base, technology


stone_progress_tree = [
    [None, technology.stone_militia, None],
    [technology.stone_home, None, technology.stone_hut],

]

bronze_progress_tree = [
    [None, technology.bronze_home_1, None],
    [technology.bronze_pottery, technology.bronze_sawmil, technology.bronze_spearman],
    [None, technology.bronze_forager, None],
    [technology.bronze_plantation, technology.bronze_winery, technology.bronze_archer],
    [technology.bronze_home_3, None, technology.bronze_home_2],
]

iron_progress_tree = [
    [None, technology.IronHome_1, None],
    [technology.IronFoundry, None, technology.IronForger],
    [technology.IronLegionary, None, technology.IronRider],
    [None, technology.IronFelting, None],
    [None, technology.IronHome_2, None],
    [technology.IronButcher, None, technology.IronJewelry],
    [None, technology.IronHome_3, None],
]


