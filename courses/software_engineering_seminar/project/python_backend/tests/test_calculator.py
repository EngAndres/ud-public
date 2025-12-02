import pytest
import Calculator

@pytest.fixture
def calc():
    return Calculator()

def test_sum(calc):
    a = 5
    b = 3
    c = 8
    assert calc.sum(a, b) == c

@pytest.mark.parametrize(
    "a", "b", "expected_result",
    [
        (5, 3, 8),
        (0, 0, 0),
        (-1, 1, 0),
        (2.5, 2.5, 5.0),
        (-2, -3, -5)
    ]
)
def test_sum_mutilple(calc, a, b, expected_result):
    assert calc.sum(a, b) == expected_result

def test_sum_character(calc, a, b_string):
    assert calc.sum(a, b_string) == ValueError()
