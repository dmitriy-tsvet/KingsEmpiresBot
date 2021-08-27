from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .check_registration import CheckUserRegistration
from .finance_regulator import FinanceRegulator


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckUserRegistration())
    dp.middleware.setup(FinanceRegulator())

