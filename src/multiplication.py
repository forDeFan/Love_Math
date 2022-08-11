from random import randint
from typing import Tuple

from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

import src.constants as const
from src.helpers.ui_helpers import Ui_Helpers as ui_hlp
from src.abstract.calculation_abstract import Calculation_Abstract


class Multiply(Calculation_Abstract, Screen):
    """
    Class for multiplication table.
    Used in multiplication_screen.kv.
    """

    # Taken from kv file.
    asked_question_no = NumericProperty(1)

    def generate_num(self, nums_range: Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[int, int]:
        """
        Generate 2 random numbers and return it in Tuple.

        Args:
            nums_range:
                range for randint to generate two numbers.

        Returns:
            Tuple[int, int]: generated numbers.
        """
        num1 = randint(nums_range[0][0], nums_range[0][1])
        num2 = randint(nums_range[1][0], nums_range[1][1])
        return num1, num2

    def set_num(self, ids_to_set: Tuple[str, str], generated_nums: Tuple[int, int] = None) -> None:
        """
        Set numbers in UI at multiplication_screen.kv. Numbers will be used for multiplication.

        This function used only when correct answer given or at first app run to populate numbers if UI fields empty.
        If leaving screen or wrong answer - numbers stay unchanged until task completed succesfullfy by user.

        Args:
            ids_to_set (Tuple[str]): 
                Tuple of id's from kv screen - from which numbers for multiplication are taken/ or set if empty.

            genearated_nums (Tuple[int, int]):
                Numbers are generated at first app start or when good answer.
                If generated_nums != None: values from generated_nums will be inserted in UI fields at multiplication_screen.kv.
                Defaults to None.
        """
        num1 = ids_to_set[0]
        num2 = ids_to_set[1]

        if num1.text == "":
            first_nums = self.generate_num(
                nums_range=const.MULTIPLICATION_SCREEN_RANGE)
            num1.text = str(first_nums[0])
            num2.text = str(first_nums[1])
        elif generated_nums != None:
            num1.text = str(generated_nums[0])
            num2.text = str(generated_nums[1])

    def good_answer(self) -> None:
        """
        If good answer change UI in multiplication_screen.kv.

        Affect UI elements with id's:
            result_label
            check_button
            multiplication_result
        """
        ui_hlp.change_label_ui(self, label=self.ids.result_label, l_col=const.GREEN,
                               l_out_wid="3dp", l_txt="Dobrze :)", l_f_size="30dp")
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=True
        )
        ui_hlp.hide_widget(
            self, self.ids.multiplication_result, dohide=True
        )
        # Clear messages, generate new quest.
        Clock.schedule_once(
            lambda dt: self.new_ui_setup(),
            2,
        )

    def wrong_answer(self) -> None:
        """
        If wrong answer change UI in multiplication_screen.kv.

        Affect UI elements with id's:
            result_label
            check_button
            multiplication_result.text
        """
        ui_hlp.change_label_ui(self, label=self.ids.result_label, l_col=const.RED,
                               l_out_wid="0.8dp", l_txt="Żle! Spróbuj jeszcze raz", l_f_size="20dp")
        self.ids.multiplication_result.text = ""
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=True
        )
        # Check button enable.
        Clock.schedule_once(
            lambda dt: ui_hlp.disable_widget(
                wid=self.ids.check_button, is_disabled=False
            ),
            2,
        )

    def new_ui_setup(self) -> None:
        """
        Arrange UI of multiplication_screen.kv for new multiplication task.
        Strongly conneccted with sreen ids.

        Changes params of UI:
            result_label,
            multiplication_result,
            check_button.
        """
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=False
        )
        ui_hlp.hide_widget(
            self, self.ids.multiplication_result, dohide=False
        )
        ui_hlp.change_label_ui(self, label=self.ids.result_label, l_col=const.BLACK,
                               l_out_wid="0dp", l_txt="Wpisz wynik", l_f_size="15dp")
        self.ids.multiplication_result.text = ""

    def show_result(self, num_ids: Tuple[str, str], nums_range: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
        """
        Notify user in UI multiplication_screen.kv about right/ wrong result.
        If correct answer arrange new multiplication task in UI.

        Changes params of UI:
            result_label,
            multiplication_result,
            multiplication_result.text,
            check_button.

        Args:
            num_ids (List[str]): numbers taken from id's fields in kv file.
            nums_range (List[Tuple[int, int]]): range used by randint for numbers generation.

        Returns:
            bool (to notify Results.update_result()):
            True if correct answer,
            False if wrong answer.
        """
        # Unfocus textfield on android in order to receive key input.
        if platform == "android":
            from src.helpers.android_helpers import Android_Helpers as an_hlp

            an_hlp.unfocuser(self)

        user_result = self.ids.multiplication_result.text
        computed_result = int(num_ids[0].text) * int(num_ids[1].text)
        self.asked_question_no += 1

        if user_result == str(computed_result):
            self.good_answer()
            self.set_num(ids_to_set=[num_ids[0], num_ids[1]], generated_nums=self.generate_num(
                nums_range=nums_range))
            return True
        else:
            self.wrong_answer()
            return False
