from aiogram.dispatcher.filters.state import StatesGroup, State


class Contest(StatesGroup):
    set_capture_units = State()
    start_capture = State()
    add_units_in_camp = State()
