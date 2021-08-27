from utils.db_api import tables, db_api
from utils.ages import models
import json
import typing
import random


if __name__ == "__main__":

    session = db_api.NewSession()

    session.session.query(tables.Citizens).all()


    session.close()



