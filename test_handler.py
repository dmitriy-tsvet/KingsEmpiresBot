from utils.db_api import tables, db_api
from utils.models import models
import json
import typing
import random
import re
from sqlalchemy import desc, asc, or_

current_session = db_api.CreateSession()

buildings: tables.Buildings = current_session.db.query(
    tables.Buildings).filter_by(user_id=615311497).first()

player_buildings = list(buildings.buildings[0])

player_buildings[1] = 1

buildings.buildings = [player_buildings]

current_session.close()


