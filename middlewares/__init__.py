from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .check_registration import CheckUserRegistration


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckUserRegistration())

