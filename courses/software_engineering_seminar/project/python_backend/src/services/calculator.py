"""
This module has a class to represents the behavior of a 
typical calculator.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

class Calculator:
    """This is a class with the basic aritmetics operations."""

    def sum(self, num_a, num_b):
        """
        This method makes a sum between the two numbers
        passed by the parameters.

        Args:
            num_a: First number of the sum.
            num_b: Second number of the sum.

        Returns:
            The sum of the two numbers. 
        """
        return num_a + num_b

    def division(self, num_a, num_b):
        """
        This method makes a division between the two numbers
        passed by the parameters.

        Args:
            num_a: First number of the division.
            num_b: Second number of the division.

        Returns:
            The division of the two numbers. 

        Raises:
            An error when denominator is zero.
        """
        if num_b != 0:
            return num_a / num_b

        raise ValueError("Division by zero is forbiden.")
