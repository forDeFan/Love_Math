from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from src.android_helpers import Android_Helpers
from src.db_connection import Db_Connection


class Results(Screen):
    def get_result(self, db: Db_Connection, category: str) -> str:
        return str(db.get_result(category)[0])

    def update_result(
        self, db: Db_Connection, category_name: str, good_answer: bool
    ):
        if good_answer:
            db.update_result(category_name)

    def send_result_sms(self, phone: Android_Helpers):
        if platform == "android":
            print(phone.get_ph_book())
