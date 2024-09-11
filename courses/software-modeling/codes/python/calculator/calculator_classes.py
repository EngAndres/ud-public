"""
This module has class definition both abstract and concrete
for calculators.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>

This file is part of PyCalculator-UD.

PyCalculator-UD is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

PyCalculator-UD is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with PyCalculator-UD. If not, see <https://www.gnu.org/licenses/>. 
"""

from datetime import datetime
from abc import ABC, abstractmethod

class AbstractCalculator(ABC):
    """
    This class represents the behavior of an abstract calculator.
    """

    def sum(self, a: float, b: float) -> float:
        """This method sums two numerical values.

        This method takes two arguments, expected as numbers,
        and calculate and return the sum of those ones.

        Args:
            a(float): First number of the sum.
            b(float): Second number of the sum.

        Returns:
            A float value with the result of the sum.
        """
        return a + b

    def rest(self, a: float, b: float) -> float:
        """This method applies substraction between two numbers.

        This method takes two numbers received as arguments
        an calculate the substraction in the given order.

        Args:
            a(float): First number of the rest.
            b(float): Second number of the rest.

        Returns:
            A float with the result of the substraction.
        """
        return a - b

    def multiplication(self, a: float, b: float) -> float:
        """This method mutiplies two numbers.

        This method takes two numbers provided as arguments
        and calculate multiplication using native arithmetic operation.

        Args:
            a(float): First number of the multiplication.
            b(float): Second number of the multiplication.

        Return:
            A float with the result of the multiplication.
        """
        return a * b

    def division(self, a: float, b: float) -> float:
        """This method calculates the division between two numbers.

        This method takes two numbers, and calculate division using
        native arithmetic operation, but without validation of
        zero-division.

        Args:
            a(float): Numerator of the division
            b(float): Divisor of the division

        Returns:
            A float with the result of the division.
        """
        return a / b

    @abstractmethod
    def power(self, base: int, exponent: int) -> int:
        """This is an abstract method for power calculation.

        Args:
            base(int): base of the power
            exponent(int): exponent of the power

        Returns:
            An integer with the result of the power.
        """

# =============== Concrete Version of a Calculator =============== #

class SimpleCalculator(AbstractCalculator):
    """
    This class represents the behavior of a simple concrete calculator
    where methods from abstract class are ihnerated, some improvements
    and new functionalities are added.
    """

    def __init__(self):
        self.memory = 0

    def division(self, a: float, b: float) -> float:
        """This method calculates the division between two numbers.

        This method takes two numbers, and calculate division using
        native arithmetic operation, including validation of
        zero-division.

        Args:
            a(float): Numerator of the division
            b(float): Divisor of the division

        Returns:
            A float with the result of the division.
        """
        try:
            result = a / b
        except Exception as e:
            print(f"ERROR. {e}")
            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()} --- ERROR. {e}.")
            result = None
        return result

    def power(self, base: int, exponent: int) -> int:
        """This is a method for power calculation.

        In this method the power is calculated using a loop
        to apply multiplication in an iterative way.

        Args:
            base(int): base of the power
            exponent(int): exponent of the power

        Returns:
            An integer with the result of the power.
        """
        if exponent == 0:
            result = 1
        else:
            temp = 1
            # java => for(int i = 0; i < exponent; i++)
            for i in range(exponent):
                temp *= base
            result = temp
        return result
