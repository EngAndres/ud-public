"""
This file has an example of a Calculator file.

Author: Carlos A Sierra <cavirguezs@udistrital.edu.co> - Abr/2025
"""
class Calc:
    """This is an example of a calculator as an object"""

    def __init__(self):
        self.memory = 0.0

    def sum (self, a1: float, b2: float) -> float:
        """This method makes an addition to another number.
        
        Args:
            a1(float): First number in the addition
            b2(float): Second number in the addition

        Returns:
            The sum of the two numbers.
        """
        return a1 + b2

    def substract(self, num1: float, num2: float) -> float:
        """
        This method makes a substraction of the second
        number from the first number.
        
        Args:
            num1(float): First number of the substraction
            num2(float): Second number of the substraction

        Returns:
            The result of the substraction.
        """
        return num1 - num2

    def multiplication(self, num1: float, num2: float) -> float:
        """
        This method multiplies two numbers.

        Args:
            num1(float): First number of the multiplication
            num2(float): Second number of the multiplication

        Returns:
            The result of the multiplication
        """
        return num1 * num2

    def division(self, num1: float, num2: float) -> float:
        """
        This method makes the division of two numbers.
        
        Args:
            num1(float): Enumerator of the division
            num2(float): Denominator of the division

        Returns:
            The result of the division.
        """
        try:
            return num1 / num2
        except Exception as e:
            print(f"Error in division. {e}")
