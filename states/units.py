from aiogram.dispatcher.filters.state import StatesGroup, State


class Units(StatesGroup):
    menu = State()
    about_unit = State()
    create_unit = State()
