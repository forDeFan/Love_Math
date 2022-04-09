from random import randint
from typing import Tuple

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


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
        self.hide_widget(self.ids.check_button, dohide=False)
        self.hide_widget(self.ids.multiplication_result, dohide=False)
        self.ids.result_card.outline_color = (0, 0, 0, 0)
        self.ids.result_card.outline_width = "0dp"
        self.ids.multiplication_result.text = ""
        self.ids.result_card.text = "Wpisz wynik"
        self.ids.result_card.font_size = "15dp"
        self.set_nums()

    def show_result(self) -> bool:
        user_result = self.ids.multiplication_result.text
        computed_result = int(self.ids.num1.text) * int(
            self.ids.num2.text
        )

        if user_result == str(computed_result):
            self.ids.result_card.outline_color = (
                181 / 255,
                255 / 255,
                235 / 255,
                1,
            )
            self.ids.result_card.outline_width = "4dp"
            self.ids.result_card.font_size = "60dp"
            self.ids.result_card.text = "Dobrze :)"
            self.hide_widget(self.ids.check_button, dohide=True)
            self.hide_widget(
                self.ids.multiplication_result, dohide=True
            )
            Clock.schedule_once(
                lambda dt: self.new_multiplication_setup(), 2
            )
            return True
        else:
            self.ids.result_card.outline_color = (
                255 / 255,
                3 / 255,
                3 / 255,
                1,
            )
            self.ids.result_card.outline_width = "0.8dp"
            self.ids.result_card.text = "Żle! Spróbuj jeszcze raz!"
            self.ids.multiplication_result.text = ""
            return False

    def hide_widget(self, wid, dohide=True):
        if hasattr(wid, "saved_attrs"):
            if not dohide:
                (
                    wid.height,
                    wid.size_hint_y,
                    wid.opacity,
                    wid.disabled,
                ) = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = (
                wid.height,
                wid.size_hint_y,
                wid.opacity,
                wid.disabled,
            )
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = (
                0,
                None,
                0,
                True,
            )
