import os

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp

from src.db_connection import Db_Connection
from src.multiplication import Multiply
from src.ui_helpers import Ui_Helpers


class Main_App(MDApp):
    def build(self):
        # Get android permissions if run on android.
        if platform == "android":
            from android.permissions import (
                Permission,
                request_permissions,
            )

            request_permissions(
                [
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.READ_CONTACTS,
                    Permission.SEND_SMS,
                ]
            )
            from src.android_helpers import Android_Helpers

            # Set android communication interface.
            self.phone = Android_Helpers()

        # Setup app defaults details.
        self.title = "I LoVE MatH"
        self.theme_cls.primary_palette = "Pink"

        self.screen_manager = ScreenManager()

        # Load main screen at app startup.
        self.screen_manager.add_widget(
            Builder.load_file("kv/main_screen.kv")
        )

        # Load rest of kv's.
        self.screen_manager.add_widget(
            Builder.load_file("kv/multiplication_screen.kv")
        )

        # Register custom classes tp use them in kv's.
        Factory.register(Multiply, "Multiply")
        Factory.register(Ui_Helpers, "Ui_Helpers")

        # Start global DB.
        self.db = Db_Connection(
            "my.db",
            "multiply",
            "fraction",
            "percent",
            "roman",
        )

        return self.screen_manager

    def on_start(self):
        self.screen_manager.current = "main_screen"

    def on_stop(self):
        db_file = "my.db"
        if os.path.isfile(db_file):
            os.remove(db_file)

    def update_db_result(self, category_name: str, good_answer: bool):
        if good_answer:
            self.db.update_result(category_name)

    def get_db_result(self, category_name: str) -> str:
        return str(self.db.get_result(category_name)[0])

    def send_result_sms(self, tel, msg):
        if platform == "android":
            self.phone.send_sms(tel=tel, msg=msg)


if __name__ == "__main__":
    Main_App().run()
