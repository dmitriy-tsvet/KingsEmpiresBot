from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy import create_engine

from sqlalchemy.orm import relationship, backref, sessionmaker, Session

from sqlalchemy.ext.declarative import declarative_base
from .my_sqlalchemy_type import JsonDecorator

import json

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)

    townhall = relationship("TownHall", backref=backref("user", uselist=False))
    units = relationship("Units", backref=backref("user", uselist=False))
    market = relationship("Market", backref=backref("user", uselist=False))
    clan = relationship("Clan", backref=backref("user", uselist=False))
    clan_member = relationship("ClanMember", backref=backref("user", uselist=False))
    clan_invitation = relationship("ClanInvitation", backref=backref("user", uselist=False))
    progress = relationship("Progress", backref=backref("user", uselist=False))
    manufacture = relationship("Manufacture", backref=backref("user", uselist=False))


class TownHall(Base):
    __tablename__ = "townhall"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    country_name = Column(String)
    age = Column(String)
    population = Column(Integer)
    money = Column(Integer)
    stock = Column(Integer)
    diamonds = Column(Integer)
    timer = Column(Integer)


class Buildings(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    buildings = Column(JsonDecorator)
    clan_building_lvl = Column(Integer)
    build_timer = Column(JsonDecorator)
    timer = Column(Integer)


class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    score = Column(Integer)
    score_timer = Column(Integer)
    tree = Column(JsonDecorator)
    unlocked_buildings = Column(JsonDecorator)


class Manufacture(Base):
    __tablename__ = "manufacture"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    storage = Column(JsonDecorator)
    creation_queue = Column(JsonDecorator)
    wait_queue = Column(JsonDecorator)


class Units(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    units_type = Column(JsonDecorator)
    units_count = Column(JsonDecorator)
    real_units_count = Column(Integer)
    creation_queue = Column(JsonDecorator)


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    territory_owned = Column(JsonDecorator)
    territory_captures = Column(JsonDecorator)


class Market(Base):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    product = Column(String)
    count = Column(Integer)
    price = Column(Integer)
    timer = Column(Integer)


class Clan(Base):
    __tablename__ = "clan"

    clan_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    emoji = Column(String)
    rating = Column(Integer)
    units = Column(Integer)
    money = Column(Integer)
    creator = Column(Integer, ForeignKey("user.user_id"))
    contest_count = Column(Integer)
    state = Column(String)

    clan_member = relationship("ClanMember", backref="clan")
    clan_invitation = relationship("ClanInvitation", backref="clan", uselist=False)


class ClanMember(Base):
    __tablename__ = "clan_member"

    id = Column(Integer, primary_key=True)
    clan_id = Column(Integer, ForeignKey("clan.clan_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    rank = Column(String)
    clan_units = Column(Integer)
    contest_score = Column(Integer)
    units_donate = Column(Integer)
    donate_timer = Column(Integer)


class ClanInvitation(Base):
    __tablename__ = "clan_invitation"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    clan_id = Column(Integer, ForeignKey("clan.clan_id"))
    timer = Column(Integer)

    clan: Clan


class Contest(Base):
    __tablename__ = "contest"

    id = Column(Integer, primary_key=True)
    clan_id_1 = Column(Integer, ForeignKey("clan.clan_id"))
    clan_id_2 = Column(Integer, ForeignKey("clan.clan_id"))
    recent_log = Column(JsonDecorator)
    log = Column(JsonDecorator)
    state_timer = Column(Integer)
    territory_names = Column(JsonDecorator)
    territory_owners = Column(JsonDecorator)
    territory_units = Column(JsonDecorator)
    territory_captures = Column(JsonDecorator)
    clans_rating = Column(JsonDecorator)
    colors = Column(JsonDecorator)

    clan_1 = relationship("Clan", foreign_keys=[clan_id_1])
    clan_2 = relationship("Clan", foreign_keys=[clan_id_2])


def create_session() -> Session:
    # connect_args={'timeout': 1}
    sqlite_file_path = "database.db"
    engine = create_engine("sqlite:///{}".format(sqlite_file_path))
    NewSession = sessionmaker(bind=engine)

    session: Session = NewSession()

    return session


# class UserData:
#     def __init__(self, user_id: int):
#         self.user_id = user_id
#
#         self.user_table = None
#         self.townhall_table = None
#
#         self.session = None
#         self.query = None
#
#     def open_session(self):
#         self.session = create_session()
#
#         self.query = self.session.query(User).filter(User.id == self.user_id).first()
#         self.user_table = self.query
#         self.townhall_table = self.query.townhall[0]
#
#     def insert_data(self, value):
#         self.session.add(value)
#
#     def commit(self):
#         self.session.commit()
#
#     def close_session(self):
#         self.commit()
#         self.session.close()





# if __name__ == "__main__":
#     select()
