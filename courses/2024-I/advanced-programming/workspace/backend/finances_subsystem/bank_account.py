"""
This file contains the classes and methods to manage the bank accounts of the users.

Author: Carlo A. Sierra <cavirguezs@udistrital.edu.co>
"""

class BankAccount: # pylint: disable=too-few-public-methods
    """This class represents the behavior of a bank account into the application"""

    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number
