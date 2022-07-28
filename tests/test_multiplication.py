import pytest
from pytest_mock import mocker
from src.multiplication import Multiply
from kivymd.uix import Label


class Test_Multiplication:

    @pytest.fixture
    def multiply(self):
        return Multiply()

    def test_if_random_numbers_generated(self, multiply):
        nums1 = multiply.generate_numbers()
        multiply.generate_numbers()
        nums2 = multiply.generate_numbers()

        assert nums1 != nums2

    def test_if_generated_random_numbers_at_specified_range(
        self, multiply
    ):
        r1 = range(2, 31)
        r2 = range(2, 10)
        nums = multiply.generate_numbers()

        assert nums[0] in r1
        assert nums[1] in r2

    def test_if_nums_generated_when_num1_empty_string_from_label(self, mocker, multiply):
        """
        Check if "generate_numbers" fired when num1.text = empty str.
        num1 and num2 taken from Label.text attribute.
        """
        mocked_generate_numbers = mocker.patch.object(
            multiply, 'generate_numbers')
        mocked_generate_numbers.return_value = [1, 1]
        lab = Label(text="")
        multiply.ids = {"num1": lab, "num2": lab}
        multiply.set_nums(nums=[lab.text, lab.text])

        assert multiply.ids.num1.text == "1"

    def test_if_nums_populated_when_num1_not_empty_string_from_label(self, multiply):
        """
        Check if numbers generated in UI - taken from Label.text
        """
        lab = Label(text="2")
        multiply.ids = {"num1": lab, "num2": lab}
        multiply.set_nums(nums=[lab.text, lab.text])

        assert multiply.ids.num1.text == "2"
