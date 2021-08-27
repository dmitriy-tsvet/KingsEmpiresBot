import random
from utils.db_api import db_api, tables
from utils.classes import maths
import time


class FinanceRegulator:

    @staticmethod
    def people_regulator(population: int, finance_budget: int):

        result = random.choices([0, 1], [90, 10])[0]

        result = 1
        if result == 1:
            num = maths.Maths.subtract_percent(population, 80)
            substract_num = random.randint(0, num)

            finance_budget -= substract_num
        else:
            finance_budget = 0

        if finance_budget < 1:
            num = maths.Maths.subtract_percent(population, 80)
            substract_num = random.randint(0, num)
            population -= substract_num
        else:
            population = 0

        return population, finance_budget
    #
    # @staticmethod
    # def resource_regulator(finance_balance: int, resource_balance: int):
    #     if finance_balance < 1:
    #         finance_balance = abs(finance_balance)
    #         regulate_balance -= random.randint(0, finance_balance)
    #
    #
    # @staticmethod
    # def army_regulator(finance_balance: int, regulate_balance: int):
    #     if finance_balance < 1:
    #         finance_balance = abs(finance_balance)
    #         regulate_balance -= random.randint(0, finance_balance)


