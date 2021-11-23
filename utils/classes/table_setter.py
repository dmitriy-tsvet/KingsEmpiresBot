from utils.db_api import tables, db_api
from utils.models import base, ages
from aiogram import types


class TableSetter:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def set_stone_age(self, message: types.Message, country_name: str):
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username

        user = tables.User(
            user_id=self.user_id, first_name=first_name,
            last_name=last_name, username=username,
        )
        age = ages.Age.get("Каменный Век")
        progress_tree = []

        for branch in age.progress_tree:
            new_branch = []
            for tech in branch:
                if tech is not None:
                    tech = 0
                new_branch.append(tech)
            progress_tree.append(new_branch)

        townhall = tables.TownHall(
            user_id=self.user_id,
            country_name=country_name,
            age=age.name,
            population=100,
            money=200,
            stock=200,
            diamonds=100,
            timer=None,
        )
        progress = tables.Progress(
            user_id=self.user_id,
            score=9,
            score_timer=0,
            tree=progress_tree,
            unlocked_buildings=[]
        )

        trees = ["tree" for i in range(0, 19)]
        buildings = tables.Buildings(
            user_id=self.user_id,
            buildings=[2, 0, 1, "tree", 2, "tree", None, *trees],
            clan_building_lvl=0,
            build_timer=[],
            timer=None
        )
        manufacture = tables.Manufacture(
            user_id=self.user_id,
            storage=[],
            creation_queue=[],
            wait_queue=[]
        )

        units = tables.Units(
            user_id=self.user_id,
            units_type=[None for i in range(0, 5)],
            units_count=[0 for i in range(0, 5)],
            real_units_count=0,
            creation_queue=[]
        )

        campaign = tables.Campaign(
            user_id=self.user_id,
            territory_owned=[False for i in range(0, 20)],
            territory_captures={}
        )

        session = db_api.CreateSession()

        session.db.add(user)
        session.db.add(townhall)
        session.db.add(progress)
        session.db.add(buildings)
        session.db.add(manufacture)
        session.db.add(units)
        session.db.add(campaign)

        session.close()