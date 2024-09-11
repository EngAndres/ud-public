"""
This module is an example of an abstract class to define a calculator operations.

Copyright (C) 2024  Carlos Andres Sierra <cavirguezs@udistrital.edu.co>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from datetime import datetime
from abc import ABC, abstractmethod
import numpy as np

class AbstractCalculator(ABC):
    """
    This class represents the behavior of an abstract calculator.
    """

    def sum(self, a: int, b: int) -> int:
        """This method sums two integer numbers.

        In this method a couple of integers are taken and sum had been calculated
        independing of size and sign.
        
        Args:
            a (int): Fisrt number to be used in the addition.
            b (int): Second number to be used in the addition.

        Returns:
            An integer with the result of sum the arguments given.
        """
        return a + b

    @abstractmethod
    def division(self, a: float, b: float) -> float:
        """This is an abstract method to force childs to implement division.

        Each calculator can define its own division process, so here just an
        abstract definition is requiered.

        Args:
            a(float): Numerator of the division.
            b(float): Divisor of the division.

        Returns:
            A float number with the result of the division.
        """

#========================= Concrete Calculator =====================#

class Calculator(AbstractCalculator):
    """This an example of a simple concrete calculator."""

    def __init__(self):
        self.memory = 0

    def division(self, a: float, b: float):
        """This is a concrete version of a typical division.

        This method implements a simple division between two numbers but 
        a validation to avoid zero-division is applied.

        Args:
            a(float): Numerator of the division.
            b(float): Divisor of the division.

        Returns:
            A float with the result of the division, or an error.

        Raise:
            An error will arise when denomitor will be zero.
        """
        try:
            result = a / b
        except Exception as e:
            print(f"ERROR. {e}")
            with open('log.txt', 'a', encoding='utf-8') as file:
                file.write(f"{datetime.now()}. Division by zero.")
            result = np.nan
        return result


#========================= Client CLI =====================#
if name == "__main__":
    MENU = """1. Realizar Suma
    2. Realizar división
    3. Salir\n"""

    # create an instance of a calculator
    calculator = Calculator()

    option = input(MENU)
    while option != 3:
        if option == 1:
            a = input("Provide first number of the sum:")
            b = input("Provide second number of the sum:")
            print(f"Result: {calculator.sum(a, b)}")
        elif option == 2:
            a = input("Provide numerator of the division:")
            b = input("Provide divisor of the division:")
            print(f"Result: {calculator.division(a, b)}")
        else:
            print("Please, choose a valid option.\n")

        option = input(MENU) # avoid infinite loop
