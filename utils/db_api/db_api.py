from utils.db_api import tables
from sqlalchemy.orm import Session


class CreateSession:
    def __init__(self):
        self.db: Session = tables.create_session()

    def filter_by_user_id(self, user_id: int, table):
        query = self.db.query(table).filter(
            table.user_id == user_id).first()

        return query

    def close(self):
        if self.db is not None:
            self.db.commit()
            self.db.close()
