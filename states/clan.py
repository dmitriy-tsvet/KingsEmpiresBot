from aiogram.dispatcher.filters.state import StatesGroup, State


class Clan(StatesGroup):
    set_name = State()
    set_description = State()
    set_emoji = State()


