from aiogram.dispatcher.filters.state import StatesGroup, State


class Buildings(StatesGroup):
    menu = State()
    home_buildings = State()
    some_buildings = State()
    about_building = State()


