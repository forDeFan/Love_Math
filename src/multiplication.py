from random import randint
from typing import Tuple

from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from src.ui_helpers import Ui_Helpers as hel


class Multiply(Screen):
    """
    Class for multiplication table - used in multiplication_screen.kv.
    """

    # Number of asked questions.
    mul_q_counter = NumericProperty(1)

    def generate_numbers(self) -> Tuple[int, int]:
        """
        Generate 2 random numbers for UI to be multiplied.
        Range of num1 2 - 30
        Range of num2 2 - 9

        Returns:
            Tuple[int, int]: [random_num1, random_num2]
        """
        num1 = randint(2, 30)
        num2 = randint(2, 9)
        return num1, num2

    def set_nums(self, nums=None) -> None:
        """
        Set numbers from generate_numbers() in UI at multiplication_screen.kv - to be multiplied by user.
        Used only when correct answer given or at first app run.
        If leaving screen or wrong answer - will not populate fields.

        Args:
            nums (str(int)): Defaults to None.
            If nums != None: insert values from nums in UI fields.

        """
        num1 = self.ids.num1.text
        if num1 == "":
            nums = self.generate_numbers()
            self.ids.num1.text = str(nums[0])
            self.ids.num2.text = str(nums[1])
        elif nums != None:
            self.ids.num1.text = str(nums[0])
            self.ids.num2.text = str(nums[1])

    def new_multiplication_setup(self):
        """
        If proper answer - clear fields and make new UI setup.
        """
        hel.disable_widget(wid=self.ids.check_button, is_disabled=False)
        # hel.hide_widget(self, self.ids.check_button, dohide=False)
        hel.hide_widget(
            self, self.ids.multiplication_result, dohide=False
        )
        self.ids.result_label.outline_color = (0, 0, 0, 0)
        self.ids.result_label.outline_width = "0dp"
        self.ids.multiplication_result.text = ""
        self.ids.result_label.text = "Wpisz wynik"
        self.ids.result_label.font_size = "15dp"

    def show_result(self) -> bool:
        """
        If multiplication correct/ wrong show UI message.
        If correct fire new_multiplication_setup().

        Returns:
            bool: to notify Results.update_result()
        """
        user_result = self.ids.multiplication_result.text
        computed_result = int(self.ids.num1.text) * int(
            self.ids.num2.text
        )
        self.mul_q_counter += 1
        # Good answer.
        if user_result == str(computed_result):
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
            hel.disable_widget(
                wid=self.ids.check_button, is_disabled=True
            )
            # hel.hide_widget(self, self.ids.check_button, dohide=True)
            hel.hide_widget(
                self, self.ids.multiplication_result, dohide=True
            )
            # Clear messages, generate new quest.
            Clock.schedule_once(
                lambda dt: self.new_multiplication_setup(),
                2,
            )
            self.set_nums(self.generate_numbers())
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
            self.ids.multiplication_result.text = ""
            hel.disable_widget(
                wid=self.ids.check_button, is_disabled=True
            )
            # Check button.
            Clock.schedule_once(
                lambda dt: hel.disable_widget(
                    wid=self.ids.check_button, is_disabled=False
                ),
                2,
            )
            return False
