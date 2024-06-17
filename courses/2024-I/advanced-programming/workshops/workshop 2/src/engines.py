"""
This file has a class Engine to represent all possible
engines for all the vehicles.

Author: Carlos Siera - Mar13/2024 <cavirguezs@udistrital.edu.co>
"""

class Engine:  # pylint: disable=too-few-public-methods
    """This class represents the behavior of a vehicle engine."""

    def __init__(self, name: str, type_motor: str, potency: int, weight: float):
        """
        Constructor of the class.

        Parameters:
        - name (str): Name of the engine
        - type_motor (str): Type of the engine
        - potency (int): Value of the potency
        - weight (float): Current weight of the engine
        """
        self.name = name
        self.type_ = type_motor
        self.potency = potency
        self.weight = weight

    def __str__(self):
        return f"Name: {self.name}   Type: {self.type_}\
            Potency: {self.potency}   Weight: {self.weight}"
