from random import randint
from typing import Tuple

import roman
from kivy.properties import NumericProperty
from kivy.utils import platform

import src.helpers.constants as const
from src.abstract.calculation_abstract import Calculation_Abstract
from src.answer_checker import Answer_Checker


class Roman_Nums(Calculation_Abstract, Answer_Checker):
    """ 
    Class for roman numbers.
    Used in roman_nums_screen.kv
    """

    # Taken from kv file.
    asked_question_no = NumericProperty(1)

    def generate_num(self, nums_range: Tuple[int, int]) -> str:
        """
        Generate random number in roman literal.

        Args:
            nums_range (Tuple[int, int]): range for randint to generate two numbers.

        Returns:
            str: roman literal of random generated number
        """
        return roman.toRoman(randint(nums_range[0], nums_range[1]))

    def set_num(self, ids_to_set: str, generated_nums: str = None) -> None:
        """
        Set number in UI at roman_numbers_screen.kv.

        This function used only when correct answer given or at first app run to populate it if UI field empty.
        If leaving screen or wrong answer - roman number stay unchanged until task completed succesfullfy by user.

        Args:
            ids_to_set (str): id's taken from kv file to be changed.
            generated_nums (str, optional): 
                Randomly generated roman number literal. 
                Defaults to None.
        """
        n = ids_to_set
        if n.text == "":
            n.text = self.generate_num(
                nums_range=const.ROMAN_NUMBERS_SCREEN_RANGE)
        elif generated_nums != None:
            n.text = generated_nums

    def show_result(self, ids_to_set, nums_range: Tuple[int, int]) -> bool:
        """
        Notify user in UI roman_number_screen.kv about right/ wrong result.
        If correct answer arrange new roman task in UI.

        Changes params of UI:
            result_label,
            result_text,
            result_text.text,
            check_button.

        Args:
            ids_to_set (_type_): id from kv file to be changed.
            nums_range (Tuple[int, int]): Range for number generation by randint.

        Returns:
            bool (to notify Results.update_result() in kv file):
                True if good answer.
                False when wrong answer.
                No bool returned when number/ char used by user in answer field - instead of number.
        """
        if platform == "android":
            from src.helpers.android_helpers import Android_Helpers as an_hlp

            an_hlp.unfocuser(self)

        try:
            user_result = int(self.ids.result_text.text)
            computed_result = roman.fromRoman(self.ids.roman_num.text)
            self.asked_question_no += 1

            if user_result == computed_result:
                self.set_num(ids_to_set=ids_to_set, generated_nums=self.generate_num(
                    nums_range=(nums_range[0], nums_range[1])))
                self.good_answer()
                return True
            else:
                self.wrong_answer()
                return False
        except ValueError:
            self.wrong_value()
