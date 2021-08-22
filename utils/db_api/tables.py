from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy import create_engine

from sqlalchemy.orm import relationship, backref, sessionmaker

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
    mention = Column(String)

    townhall = relationship("TownHall", backref=backref("user", uselist=False))
    units = relationship("Units", backref=backref("user", uselist=False))
    territory = relationship("Territory", backref=backref("user", uselist=False))
    food_buildings = relationship("FoodBuildings", backref=backref("user", uselist=False))
    stock_buildings = relationship("StockBuildings", backref=backref("user", uselist=False))
    citizens = relationship("Citizens", backref=backref("user", uselist=False))


class TownHall(Base):
    __tablename__ = "townhall"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    country_name = Column(String)
    age = Column(String)
    money = Column(Integer)
    timer = Column(Integer)
    food = Column(Integer)
    stock = Column(Integer)
    energy = Column(Integer)
    graviton = Column(Integer)


class Units(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    all_unit_counts = Column(Integer)
    unit_counts = Column(JsonDecorator)
    creation_queue = Column(JsonDecorator)
    creation_timer = Column(JsonDecorator)
    creation_value = Column(Integer)
    levels = Column(JsonDecorator)
    upgrade_timer = Column(Integer)
    unit_num = Column(Integer)


class Territory(Base):
    __tablename__ = "territory"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    tax_timer = Column(Integer)
    capture_timer = Column(Integer)
    owned_territory = Column(JsonDecorator)
    capturing_index = Column(Integer)
    capture_state = Column(String)


class FoodBuildings(Base):
    __tablename__ = "food_buildings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    count_buildings = Column(Integer)
    levels = Column(JsonDecorator)
    timer = Column(Integer)
    build_timer = Column(Integer)
    build_num = Column(Integer)

    def __str__(self):
        return "food"


class StockBuildings(Base):
    __tablename__ = "stock_buildings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    count_buildings = Column(Integer)
    levels = Column(JsonDecorator)
    timer = Column(Integer)
    build_timer = Column(Integer)
    build_num = Column(Integer)

    def __str__(self):
        return "stock"


class Citizens(Base):
    __tablename__ = "citizens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    population = Column(Integer)
    capacity = Column(Integer)
    creation_queue = Column(Integer)
    creation_timer = Column(Integer)
    home_counts = Column(Integer)
    build_timer = Column(Integer)
    build_num = Column(Integer)


def create_session():
    # connect_args={'timeout': 1}
    sqlite_file_path = "database.db"
    engine = create_engine("sqlite:///{}".format(sqlite_file_path))
    Session = sessionmaker(bind=engine)

    session = Session()

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
