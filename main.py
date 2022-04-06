import os

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp


class Main_App(MDApp):
    def build(self):
        # Setup app defaults details.
        self.title = "I LoVE MatH"
        self.theme_cls.primary_palette = "Pink"

        self.screen_manager = ScreenManager()
        # Load all files from kv folder and add to manager.
        kv_files = os.listdir("kv")
        for f in kv_files:
            self.screen_manager.add_widget(Builder.load_file("kv/" + f))

        return self.screen_manager


if __name__ == "__main__":
    Main_App().run()
