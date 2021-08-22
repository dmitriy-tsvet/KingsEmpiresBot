from aiogram.dispatcher.filters.state import StatesGroup, State


class Townhall(StatesGroup):
    menu = State()
    progress = State()
    citizens = State()


