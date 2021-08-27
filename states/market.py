from aiogram.dispatcher.filters.state import StatesGroup, State


class Market(StatesGroup):
    products_list = State()
    current_product = State()

