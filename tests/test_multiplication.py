import pytest
from src.multiplication import Multiply


class Test_Multiplication:
    @pytest.fixture()
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
