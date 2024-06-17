"""
This file has some classes related to engines, inclusing types.


Author: Carlos Sierra - cavirguezs@udistrital.edu.co
"""

# pylint: disable=too-few-public-methods
class Engine:
    """This class represents an abstraction of an engine for any vehicle."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        torque: int,
        maximum_speed: int,
        dimenssions: str,
        power: int,
        stability: str,
        weight: float,
    ):
        self.torque = torque
        self.maximum_speed = maximum_speed
        self.dimenssions = dimenssions
        self.power = power
        self.stability = stability
        self.weight = weight

class GasEngine(Engine):
    """This class represents the behavior of a gas engine"""

class ElectricEngine(Engine):
    """This class represents the behavior of an electric engine"""
    