from random import randint
from typing import Tuple

from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

import src.constants as const
from src.abstract.calculation_abstract import Calculation_Abstract
from src.answer_checker import Answer_Checker


class Multiply(Calculation_Abstract, Screen, Answer_Checker):
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

        try:
            user_result = self.ids.result_text.text
            computed_result = int(
                num_ids[0].text) * int(num_ids[1].text)
            self.asked_question_no += 1

            if user_result == str(computed_result):
                self.set_num(ids_to_set=[num_ids[0], num_ids[1]], generated_nums=self.generate_num(
                    nums_range=nums_range))
                self.good_answer()
                return True
            else:
                self.wrong_answer()
                return False
        except ValueError:
            self.wrong_value()
