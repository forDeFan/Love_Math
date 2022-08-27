import operator
from random import randint
from typing import Tuple

from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

import src.helpers.constants as const
from src.abstract.calculation_abstract import Calculation_Abstract
from src.answer_checker import Answer_Checker


class Add_Substract(Calculation_Abstract, Screen, Answer_Checker):
    """
    Class for add/ substraction.
    Used in add_substract_screen.kv.
    """

    # Taken from kv file.
    asked_question_no = NumericProperty(1)

    def generate_num(self, nums_range: Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[int, int]:
        num1 = randint(nums_range[0][0], nums_range[0][1])
        num2 = randint(nums_range[1][0], nums_range[1][1])
        return num1, num2

    def set_num(self, ids_to_set: Tuple[str, str], generated_nums: Tuple[int, int] = None) -> None:
        num1 = ids_to_set[0]
        num2 = ids_to_set[1]

        if num1.text == "":
            first_nums = self.generate_num(
                nums_range=const.ADD_SUBSTRACT_SCREEN_RANGE)
            num1.text = str(first_nums[0])
            num2.text = str(first_nums[1])
        elif generated_nums != None:
            num1.text = str(generated_nums[0])
            num2.text = str(generated_nums[1])

    def set_operation_type(self, num1_id: str, num2_id: str) -> str:
        if int(num1_id.text) < int(num2_id.text):
            self.ids.operation_type.text = "+"
        else:
            self.ids.operation_type.text = "-"

    @staticmethod
    def calculate(operator_id: str, num_ids: Tuple[str, str]) -> int:
        allowed_operators = {
            "+": operator.add,
            "-": operator.sub}

        calculation = allowed_operators[operator_id](int(
            num_ids[0].text), int(num_ids[1].text))
        return calculation

    def show_result(self, num_ids: Tuple[str, str], nums_range: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
        # Unfocus textfield on android in order to receive key input.
        if platform == "android":
            from src.helpers.android_helpers import Android_Helpers as an_hlp

            an_hlp.unfocuser(self)

        try:
            # TODO Add exception handling when not int
            user_result = int(self.ids.result_text.text)
            computed_result = self.calculate(
                operator_id=self.ids.operation_type.text, num_ids=num_ids)
            self.asked_question_no += 1

            if user_result == computed_result:
                self.set_num(ids_to_set=[num_ids[0], num_ids[1]], generated_nums=self.generate_num(
                    nums_range=nums_range))
                self.set_operation_type(
                    num1_id=num_ids[0], num2_id=num_ids[1])
                self.good_answer()
                return True
            else:
                self.wrong_answer()
                return False
        except ValueError:
            self.wrong_value()
