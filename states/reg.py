from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    input_name_country = State()

