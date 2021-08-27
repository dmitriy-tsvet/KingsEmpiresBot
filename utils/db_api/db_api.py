from utils.db_api import tables
from sqlalchemy.orm import Session


class NewSession:
    def __init__(self):
        self.session: Session = tables.create_session()

    def filter_by_user_id(self, user_id: int, table):
        query = self.session.query(table).filter(
            table.user_id == user_id).first()

        return query

    def close(self):
        if self.session is not None:
            self.session.commit()
            self.session.close()
