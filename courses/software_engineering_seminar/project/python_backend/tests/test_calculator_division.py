import pytest

import Calculator

class TestCalculatorDivision:

    def setup_method(self):
        self.calculator = Calculator()

    def test_division_positive_numbers(self):
        num_1, num_2 = 20, 5
        expected_result = 4.0
        result = self.calculator.division(num_1, num_2)
        assert result == expected_result
        assert isinstance(result, float)

    def test_division_negative_numbers(self):
        num_1, num_2 = -20, -5
        expected_result = 4.0
        result = self.calculator.division(num_1, num_2)
        assert result == expected_result

    def test_division_by_zero(self):
        num_1, num_2 = 20, 0
        with pytest.raises(ValueError) as ex:
            self.calculator.division(num_1, num_2)
        
        assert "Division by zero is forbiden." in str(ex.value)
