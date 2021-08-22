from aiogram.dispatcher.filters.state import StatesGroup, State


class Territory(StatesGroup):
    menu = State()
    select_territory = State()
    select_units = State()
    waiting_capture = State()
    lobby = State()
    riot = State()

