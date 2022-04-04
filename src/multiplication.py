from random import randint
from typing import Tuple

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

    def check_result(self, result: str) -> bool:
        # Values from .kv file.
        computed = int(self.ids.num1.text) * int(self.ids.num2.text)
        # From str to int.
        if result == str(computed):
            return True
        else:
            return False
