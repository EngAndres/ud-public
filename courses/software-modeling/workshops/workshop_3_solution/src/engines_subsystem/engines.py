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
        self.__torque = torque
        self.__maximum_speed = maximum_speed
        self.__dimenssions = dimenssions
        self.__power = power
        self.__stability = stability
        self.__weight = weight

    def __str__(self) -> str:
        return f"Engine: torque={self.__torque}, \
                maximum_speed={self.__maximum_speed}, \
                dimenssions={self.__dimenssions}, \
                power={self.__power}, \
                stability={self.__stability}, \
                weight={self.__weight}"


class GasEngine(Engine):
    """This class represents the behavior of a gas engine"""


class ElectricEngine(Engine):
    """This class represents the behavior of an electric engine"""
