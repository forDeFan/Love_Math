from random import randint
from typing import Tuple

from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from src.ui_helpers import Ui_Helpers as ui_hlp


class Multiply(Screen):
    """
    Class for multiplication table.
    Used in multiplication_screen.kv.
    """

    # Number of asked questions.
    mul_q_counter = NumericProperty(1)

    def generate_numbers(self) -> Tuple[int, int]:
        """
        Generate 2 random numbers for UI to be multiplied.
        Range of num1 2 - 30
        Range of num2 2 - 9

        Returns:
            Tuple[int, int]: [num1, num2]
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
            nums (str(int)):
                Defaults to None.
                If nums != None: insert values from nums in UI fields.

        """
        num1 = self.ids.num1.text
        if num1 == "":
            first_nums = self.generate_numbers()
            self.ids.num1.text = str(first_nums[0])
            self.ids.num2.text = str(first_nums[1])
        elif nums != None:
            self.ids.num1.text = str(nums[0])
            self.ids.num2.text = str(nums[1])

    # TODO SOLID
    def new_multiplication_setup(self):
        """
        Arrange UI of multiplication_screen.kv for new multiplication task.

        Changes params of UI:
            result_label,
            multiplication_result,
            check_button.
        """
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=False
        )
        # ui_hlp.hide_widget(self, self.ids.check_button, dohide=False)
        ui_hlp.hide_widget(
            self, self.ids.multiplication_result, dohide=False
        )
        self.ids.result_label.outline_color = (0, 0, 0, 0)
        self.ids.result_label.outline_width = "0dp"
        self.ids.multiplication_result.text = ""
        self.ids.result_label.text = "Wpisz wynik"
        self.ids.result_label.font_size = "15dp"

    # TODO extract changing label attributes into separate def/ SOLID
    def show_result(self) -> bool:
        """
        Notify user in UI multiplication_screen.kv about right/ wrong result.
        If correct answer fire new_multiplication_setup().

        Changes params of UI:
            result_label,
            multiplication_result,
            check_button.

        Returns:
            bool (to notify Results.update_result()):
                True if correct answer,
                False if wrong answer.
        """
        # Unfocus textfield on android in order to receive key input.
        if platform == "android":
            from src.android_helpers import Android_Helpers as an_hlp

            an_hlp.unfocuser(self)

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
            ui_hlp.disable_widget(
                wid=self.ids.check_button, is_disabled=True
            )
            # ui_hlp.hide_widget(self, self.ids.check_button, dohide=True)
            ui_hlp.hide_widget(
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
