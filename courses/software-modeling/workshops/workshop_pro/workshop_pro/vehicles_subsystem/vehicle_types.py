"""
This file has some classes related to the types of vehicles in the application.

Author: Carlos Sierra <cavirguezs@udistrital.edu.co>
"""

from .vehicle import Vehicle
from ..engines_subsystem import Engine


# pylint: disable=too-few-public-methods
class Helicopter(Vehicle):
    """This class represents the behavior of a helicopter into the application."""


# pylint: disable=too-few-public-methods
class Scooter(Vehicle):
    """This class represents the behavior of a scooter into the application."""


# pylint: disable=too-few-public-methods
class Motorcycle(Vehicle):
    """This class represents the behavior of a motorcycle into the application."""


class Car(Vehicle):
    """This class represents the behavior of a car into the application."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        chassis: str,
        price: float,
        engine: Engine,
        model: str,
        year: int,
        transmission: str,
        trade: str,
        combustion_type: str,
    ):
        super().__init__(chassis, price, engine, model, year)
        self.__transmission = transmission
        self.__trade = trade
        self.__combustion_type = combustion_type

    def __str__(self):
        return (
            super().__str__()
            + f"Transmission: {self.__transmission}\n\
                Trade: {self.__trade}\n\
                Combustion type: {self.__combustion_type}"
        )


class Yacht(Vehicle):
    """This class represents the behavior of a yacht into the application."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        chassis: str,
        price: float,
        engine: Engine,
        model: str,
        year: int,
        length: float,
        width: float,
        trade: float,
    ):
        super().__init__(chassis, price, engine, model, year)
        self.__length = length
        self.__width = width
        self.__trade = trade

    def __str__(self):
        return (
            super().__str__()
            + f"Length: {self.__length}\n\
                Width: {self.__width}\n\
                Trade: {self.__trade}"
        )


class Truck(Vehicle):
    """This class represents the behavior of a truck into the application."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        chassis: str,
        price: float,
        engine: Engine,
        model: str,
        year: int,
    ):
        super().__init__(chassis, price, engine, model, year)
        self.__consumption = self.__calculate_consumption()

    def __calculate_consumption(self):
        """This method calculates the consumption of the truck."""
        return (
            (1.1 * self.__engine.get_power())
            + (0.2 * self.__engine.get_weight())
            + (0.3 if self.__chassis == "A" else 0.5)
        )

    def __str__(self):
        return super().__str__() + f"Cosumption: {self.__consumption}"
