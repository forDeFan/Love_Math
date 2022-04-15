from random import randint
from typing import Tuple

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from src.helpers import Helpers as hel


class Multiply(Screen):
    def generate_numbers(self) -> Tuple[int, int]:
        num1 = randint(2, 30)
        num2 = randint(2, 9)
        return num1, num2

    def set_nums(self) -> None:
        nums = self.generate_numbers()
        self.ids.num1.text = str(nums[0])
        self.ids.num2.text = str(nums[1])

    def new_multiplication_setup(self):
        hel.hide_widget(self, self.ids.check_button, dohide=False)
        hel.hide_widget(
            self, self.ids.multiplication_result, dohide=False
        )
        self.ids.result_label.outline_color = (0, 0, 0, 0)
        self.ids.result_label.outline_width = "0dp"
        self.ids.multiplication_result.text = ""
        self.ids.result_label.text = "Wpisz wynik"
        self.ids.result_label.font_size = "15dp"
        self.set_nums()

    def show_result(self) -> bool:
        user_result = self.ids.multiplication_result.text
        computed_result = int(self.ids.num1.text) * int(
            self.ids.num2.text
        )

        if user_result == str(computed_result):
            self.ids.result_label.outline_color = (
                181 / 255,
                255 / 255,
                235 / 255,
                1,
            )
            self.ids.result_label.outline_width = "4dp"
            self.ids.result_label.font_size = "60dp"
            self.ids.result_label.text = "Dobrze :)"
            hel.hide_widget(self, self.ids.check_button, dohide=True)
            hel.hide_widget(
                self, self.ids.multiplication_result, dohide=True
            )
            Clock.schedule_once(
                lambda dt: self.new_multiplication_setup(), 2
            )
            return True
        else:
            self.ids.result_label.outline_color = (
                255 / 255,
                3 / 255,
                3 / 255,
                1,
            )
            self.ids.result_label.outline_width = "0.8dp"
            self.ids.result_label.text = "Żle! Spróbuj jeszcze raz"
            self.ids.multiplication_result.text = ""
            return False
