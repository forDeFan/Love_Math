from random import randint

import roman


class Roman_Nums:

    def generate_roman_number(self):
        return roman.toRoman(randint(1, 1500))

    def set_num(self):
        pass

    def new_roman_setup(self):
        pass

    def convert_from_roman(self, num_to_convert: str) -> int:
        return roman.fromRoman(num_to_convert)

    def check_result(self, num_to_check: str, result: int) -> bool:
        if int(roman.fromRoman(num_to_check)) == result:
            return True
        else:
            return False

    def show_result(self):
        pass
