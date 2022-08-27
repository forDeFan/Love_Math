from random import randint
from typing import Tuple

import roman
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

import src.helpers.constants as const
from src.abstract.calculation_abstract import Calculation_Abstract
from src.answer_checker import Answer_Checker


class Roman_Nums(Calculation_Abstract, Screen, Answer_Checker):

    # Taken from kv file.
    asked_question_no = NumericProperty(1)

    def generate_num(self, nums_range: Tuple[int, int]) -> str:
        return roman.toRoman(randint(nums_range[0], nums_range[1]))

    def set_num(self, ids_to_set: str, generated_nums: str = None) -> None:
        n = ids_to_set
        if n.text == "":
            n.text = self.generate_num(
                nums_range=const.ROMAN_NUMBERS_SCREEN_RANGE)
        elif generated_nums != None:
            n.text = generated_nums

    def show_result(self, ids_to_set, nums_range: Tuple[int, int]) -> bool:
        # Unfocus textfield on android in order to receive key input.
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
