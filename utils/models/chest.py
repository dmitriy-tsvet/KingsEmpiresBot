from utils.models import base

Caesar = base.Chest(
    name="🌿🗃 Сундук Цезаря",
    price=[500, 0, 0],
    content=["diamonds", "stock", "score"],
    counts=[(10, 25), (100, 250), (1, 3)],
    chances=[4, 70, 26]
)

Atilla = base.Chest(
    name="🔥🗃 Сундук Атиллы",
    price=[0, 0, 100],
    content=["money", "stock", "score"],
    counts=[(2000, 4000), (1000, 2000), (10, 20)],
    chances=[25, 35, 40]
)

Barbarossa = base.Chest(
    name="✝🗃 Сундук Барбароссы",
    price=[1500, 0, 0],
    content=["diamonds", "stock", "score"],
    counts=[(20, 35), (500, 1000), (2, 5)],
    chances=[7, 60, 33]
)

JoanArc = base.Chest(
    name="👩🏻 🗃 Сундук Жанны Дарк",
    price=[0, 0, 500],
    content=["money", "stock", "score", "builder_home"],
    counts=[(10000, 15000), (4000, 6000), (25, 40), (1, 1)],
    chances=[25, 25, 25, 25]
)

Napoleon = base.Chest(
    name="🥐🗃 Сундук Наполеона",
    price=[4000, 0, 0],
    content=["diamonds", "stock", "score", "builder_home"],
    counts=[(40, 70), (1200, 2500), (5, 8), (1, 1)],
    chances=[10, 58, 30, 2]
)

Churchill = base.Chest(
    name="🚬🗃 Сундук Черчилля",
    price=[7000, 0, 0],
    content=["diamonds", "stock", "score", "builder_home", "land"],
    counts=[(70, 100), (3000, 4500), (9, 14), (1, 1), (5, 10)],
    chances=[15, 40, 35, 5, 5]
)

SteveJobs = base.Chest(
    name="📱🗃 Сундук Стива Джобса",
    price=[0, 0, 900],
    content=["money", "stock", "score", "builder_home", "land"],
    counts=[(15000, 22000), (6000, 10000), (50, 70), (1, 1), (20, 30)],
    chances=[15, 15, 20, 25, 25]
)

