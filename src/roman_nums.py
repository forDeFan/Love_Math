from random import randint

import roman
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from src.ui_helpers import Ui_Helpers as ui_hlp


class Roman_Nums(Screen):

    # Number of asked questions.
    roman_q_counter = NumericProperty(1)

    def generate_roman_number(self) -> str:
        return roman.toRoman(randint(1, 1500))

    def set_num(self, num: str) -> None:
        n = self.ids.roman_num.text
        if n == "":
            self.ids.roman_num.text = str(self.generate_roman_number())
        elif num != None:
            self.ids.roman_num.text = num

    # TODO SOLID
    def new_roman_setup(self) -> None:
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=False
        )
        # ui_hlp.hide_widget(self, self.ids.check_button, dohide=False)
        ui_hlp.hide_widget(
            self, self.ids.roman_result, dohide=False
        )
        self.ids.result_label.outline_color = (0, 0, 0, 0)
        self.ids.result_label.outline_width = "0dp"
        self.ids.roman_result.text = ""
        self.ids.result_label.text = "Wpisz wartość"
        self.ids.result_label.font_size = "15dp"

    def convert_from_roman(self, num_to_convert: str) -> int:
        return roman.fromRoman(num_to_convert)

    def convert_to_roman(self, num_to_convert: str) -> str:
        return roman.toRoman(num_to_convert)

    # TODO implement for show_result.
    def check_result(self, num_to_check: str, result: int) -> bool:
        if int(roman.fromRoman(num_to_check)) == result:
            return True
        else:
            return False

    # TODO extract changing label attributes into separate def/ SOLID.
    def show_result(self) -> bool:
        # Unfocus textfield on android in order to receive key input.
        if platform == "android":
            from src.android_helpers import Android_Helpers as an_hlp

            an_hlp.unfocuser(self)

        user_result = int(self.ids.roman_result.text)
        computed_result = self.convert_from_roman(
            self.ids.roman_num.text)
        self.roman_q_counter += 1
        # Good answer.
        if user_result == computed_result:
            self.ids.result_label.outline_color = (
                181 / 255,
                255 / 255,
                235 / 255,
                1,
            )
            # Show message in UI to the user.
            self.ids.result_label.outline_width = "3dp"
            self.ids.result_label.font_size = "30dp"
            self.ids.result_label.text = "Dobrze :)"
            ui_hlp.disable_widget(
                wid=self.ids.check_button, is_disabled=True
            )
            # ui_hlp.hide_widget(self, self.ids.check_button, dohide=True)
            ui_hlp.hide_widget(
                self, self.ids.roman_result, dohide=True
            )
            # Clear messages, generate new quest.
            Clock.schedule_once(
                lambda dt: self.new_roman_setup(),
                2,
            )
            self.set_num(self.generate_roman_number())
            return True
        else:
            # Wrong answer.
            self.ids.result_label.outline_color = (
                255 / 255,
                3 / 255,
                3 / 255,
                1,
            )
            # Show message to the user.
            self.ids.result_label.outline_width = "0.8dp"
            self.ids.result_label.text = "Żle! Spróbuj jeszcze raz"
            self.ids.roman_result.text = ""
            ui_hlp.disable_widget(
                wid=self.ids.check_button, is_disabled=True
            )
            # Check button.
            Clock.schedule_once(
                lambda dt: ui_hlp.disable_widget(
                    wid=self.ids.check_button, is_disabled=False
                ),
                2,
            )
            return False
