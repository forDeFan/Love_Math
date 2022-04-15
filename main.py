from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from src.helpers import Helpers
from src.multiplication import Multiply


class Main_App(MDApp):
    def build(self):
        # Setup app defaults details.
        self.title = "I LoVE MatH"
        self.theme_cls.primary_palette = "Pink"
        self.screen_manager = ScreenManager()

        # Load main screen at app startup.
        self.screen_manager.add_widget(
            Builder.load_file("kv/main_screen.kv")
        )
        self.screen_manager.current = "main_screen"
        # Load rest of kv's.
        self.screen_manager.add_widget(
            Builder.load_file("kv/multiplication_screen.kv")
        )

        # Register custom classes to use in kv's.
        Factory.register(Multiply, "Multiply")
        Factory.register(Helpers, "Helpers")

        return self.screen_manager


if __name__ == "__main__":
    Main_App().run()
