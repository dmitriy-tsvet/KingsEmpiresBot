from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .check_registration import CheckUserRegistration
# from .unique_handler import UniqueHandler


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckUserRegistration())


