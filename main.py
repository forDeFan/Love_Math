import os

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp

import src.constants as const
from src.db_connection import Db_Connection
from src.multiplication import Multiply
from src.results import Results
from src.ui_helpers import Ui_Helpers


class Main_App(MDApp):
    def build(self) -> ScreenManager:
        if platform == "android":
            # Get android permissions if run on android.
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
        self.title = const.APP_NAME
        self.theme_cls.primary_palette = "Pink"

        # Register custom classes to use them in kv's.
        Factory.register(Multiply, "Multiply")
        Factory.register(Ui_Helpers, "Ui_Helpers")
        Factory.register(Results, "Results")

        # Start global DB.
        self.db = Db_Connection(const.DB_NAME, const.CATEGORIES)

        # Add global constants.
        self.const = const

        # Add global screen manager.
        self.screen_manager = ScreenManager(transition=NoTransition())
        # Var used to navigate in kv - to last screen visited.
        self.previous_screen = ""

        # Load main screen at app startup.
        self.screen_manager.add_widget(
            Builder.load_file("kv/main_screen.kv")
        )
        # Load rest of kv's.
        kv_files = os.listdir("kv")
        for f in kv_files:
            if f == "main_screen.kv":
                pass
            else:
                self.screen_manager.add_widget(
                    Builder.load_file("kv/" + f)
                )

        return self.screen_manager

    def on_stop(self) -> None:
        if os.path.isfile(const.DB_NAME):
            os.remove(const.DB_NAME)

    # TODO - dark mode ?
    def theme_switch(self, theme: str) -> None:
        # theme = "Dark"
        # self.theme_cls.theme_style = theme
        pass


if __name__ == "__main__":
    Main_App().run()
