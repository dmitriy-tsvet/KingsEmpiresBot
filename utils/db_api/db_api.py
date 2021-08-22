from utils.db_api import tables
import typing


class Session:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = None

    def open_session(self):
        self.session = tables.create_session()

    def built_in_query(self, table_model):
        query = self.session.query(table_model).filter(
            table_model.user_id == self.user_id).first()

        return query

    def quick_session(self, table_model):
        self.session = tables.create_session()

        query = self.session.query(table_model).filter(
            table_model.user_id == self.user_id).first()

        self.session.close()
        return query

    def insert_data(self, class_exemplar):
        self.session.add(class_exemplar)

    def commit(self):
        self.session.commit()

    def close_session(self):
        self.commit()
        self.session.close()
