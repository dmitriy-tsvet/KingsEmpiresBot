from utils.models import base, technology


stone_progress_tree = [
    [None, technology.StoneMilitia, None],
    [technology.StoneHome, None, technology.StoneHut],

]

bronze_progress_tree = [
    [None, technology.BronzeHome_1, None],
    [technology.BronzePottery, technology.BronzeSawmill, technology.BronzeSwordsman],
    [None, technology.BronzeForager, None],
    [technology.BronzePlantation, technology.BronzeWinery, technology.BronzeArcher],
    [technology.BronzeHome_3, None, technology.BronzeHome_2],
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


