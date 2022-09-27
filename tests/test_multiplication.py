import pytest
from kivy.uix.screenmanager import Screen
from kivymd.uix import Label
from pytest_mock import mocker
from src.abstract.calculation_abstract import Calculation_Abstract
from src.answer_checker import Answer_Checker
from src.multiplication import Multiply


class Test_Multiplication:

    @pytest.fixture
    def multiply(self):
        return Multiply()

    def test_if_multiply_is_sublcass_of_calculation_abstract(self):
        assert issubclass(Multiply, Calculation_Abstract)

    def test_if_multiply_is_subclass_screen(self):
        assert issubclass(Multiply, Screen)

    def test_if_multiply_is_subclass_of_answer_checker(self):
        assert issubclass(Multiply, Answer_Checker)

    def test_if_random_numbers_generated(self, multiply):
        test_rang = ((1, 200), (3, 400))
        nums1 = multiply.generate_num(test_rang)
        nums2 = multiply.generate_num(test_rang)

        assert nums1 != nums2

    def test_if_generated_random_numbers_at_specified_range(
        self, multiply
    ):
        r1 = range(2, 32)
        r2 = range(2, 11)
        test_rang = ((2, 31), (2, 10))
        nums = multiply.generate_num(test_rang)

        assert nums[0] in r1
        assert nums[1] in r2

    def test_if_nums_generated_when_num1_empty_string_from_label(self, mocker, multiply):
        """
        Check if "generate_numbers" fired when num1.text = empty str.
        num1 and num2 taken from Label.text attribute.
        """
        mocked_generate_numbers = mocker.patch.object(
            multiply, 'generate_num')
        mocked_generate_numbers.return_value = [1, 1]
        lab = Label(text="")
        multiply.ids = {"num1": lab, "num2": lab}
        multiply.set_num(ids_to_set=[multiply.ids["num1"], multiply.ids["num1"]],
                         generated_nums=[lab.text, lab.text])

        assert multiply.ids.num1.text == "1"

    def test_if_nums_populated_when_num1_not_empty_string_from_label(self, multiply):
        """
        Check if numbers generated in UI - taken from Label.text
        """
        lab = Label(text="2")
        multiply.ids = {"num1": lab, "num2": lab}
        multiply.set_num(ids_to_set=[
            multiply.ids["num1"], multiply.ids["num2"]], generated_nums=[lab.text, lab.text])

        assert multiply.ids.num1.text == "2"

    def test_if_user_notified_when_letter_instead_of_number_in_answer(self, mocker, multiply):
        user_literal = Label(text="n")
        num1 = Label(text="1")
        num2 = Label(text="2")
        multiply.ids = {"result_text": user_literal,
                        "num1": num1, "num2": num2}
        mock = mocker.patch.object(Multiply, "wrong_value")

        multiply.show_result(
            num_ids=(num1, num2), nums_range=None)

        mock.assert_called_once()

    def test_if_user_notified_when_good_answer(self, mocker, multiply):
        user_good_answer = Label(text="2")
        num1 = Label(text="1")
        num2 = Label(text="2")
        multiply.ids = {"result_text": user_good_answer,
                        "num1": num1, "num2": num2}
        mocker.patch.object(Multiply, "generate_num")
        mocker.patch.object(Multiply, "set_num")
        mock_g_answ = mocker.patch.object(Multiply, "good_answer")

        returned_bool = multiply.show_result(
            num_ids=(num1, num2), nums_range=None)

        mock_g_answ.assert_called_once()
        assert returned_bool == True

    def test_if_false_notified_when_wrong_answer(self, mocker, multiply):
        user_wrong_answer = Label(text="333")
        num1 = Label(text="1")
        num2 = Label(text="2")
        multiply.ids = {"result_text": user_wrong_answer,
                        "num1": num1, "num2": num2}
        mock_w_answ = mocker.patch.object(Multiply, "wrong_answer")

        returned_bool = multiply.show_result(
            num_ids=(num1, num2), nums_range=None)

        mock_w_answ.assert_called_once()
        assert returned_bool == False
