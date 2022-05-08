from kivy.uix.screenmanager import Screen
from src.db_connection import Db_Connection


class Results(Screen):
    def get_result(self, db: Db_Connection, category: str) -> str:
        return str(db.get_result(category)[0])

    def update_result(
        self, db: Db_Connection, category_name: str, good_answer: bool
    ):
        if good_answer:
            db.update_result(category_name)
