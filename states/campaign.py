from aiogram.dispatcher.filters.state import StatesGroup, State


class Campaign(StatesGroup):
    select_units = State()
