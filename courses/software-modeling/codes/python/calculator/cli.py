"""
This module has simple CLI for calculator manipulation.

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
along with Foobar. If not, see <https://www.gnu.org/licenses/>. 
"""

from calculator_classes import SimpleCalculator

if __name__ == "__main__":
    MENU = """
    1. Sumar
    2. Restar
    3. Multiplicar
    4. Dividir
    5. Potencia
    6. Salir\n
    """

    calculator = SimpleCalculator()

    option = int(input(MENU))
    while option != 6:
        if option == 1:
            a = float(input("Add first number of the sum:"))
            b = float(input("Add second number of the sum:"))
            print(f"Result: {calculator.sum(a, b)}")
        elif option == 2:
            a = float(input("Add first number of the rest:"))
            b = float(input("Add second number of the rest:"))
            print(f"Result: {calculator.rest(a, b)}")
        elif option == 3:
            a = float(input("Add first number of the multiplication:"))
            b = float(input("Add second number of the multiplication:"))
            print(f"Result: {calculator.multiplication(a, b)}")
        elif option == 4:
            a = float(input("Add first number of the division:"))
            b = float(input("Add second number of the division:"))
            print(f"Result: {calculator.division(a, b)}")
        elif option == 5:
            a = int(input("Add base of the power:"))
            b = int(input("Add exponent of the power:"))
            print(f"Result: {calculator.power(a, b)}")
        else:
            print("Please, choice a valid option.")

        option = int(input(MENU))
