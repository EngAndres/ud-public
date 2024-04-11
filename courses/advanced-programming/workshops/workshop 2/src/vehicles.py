"""
This file has a class Vehicle to represent all possible
vehicles, and also some concrete classed are define for
different vehicle types.
"""

from engines import Engine

class Vehicle:
    """
    This class represents the behavior of an abstract class
    to define vehicles.
    """

    def __init__(self, chassis: str, model: str, year: int, engine: Engine):
        """
        Constructor of the class

        Parameters:
        - chassis (str): Type of the chassis. Could be A or B.
        - model (str): name of the vehicle
        - year (int): year of the vehicle
        - engine (Engine): engine of the vehicle
        """
        if not chassis in ["A", "B"]:
            raise ValueError("This chassis is not valid.")
        if year < 1990:
            raise ValueError("The year is not a valid range.")
        self.__chassis = chassis
        self.__model = model
        self.__year = year
        self.__gas_consumption = None
        self.__engine = engine
        self._calculate_comsumption()

    def _calculate_comsumption(self):
        """This method is used to calculate internal gas consumption."""
        consumption = (
            (1.1 * self.__engine.potency)
            + (0.2 * self.__engine.weight)
            - (0.3 if self.__chassis == "A" else 0.5)
        )
        self.__gas_consumption = consumption

    def get_chassis(self) -> str:
        """
        This method is used to get the information of the vehicle' chassis.

        Returns:
        - str: the chassis of the vehicle
        """
        return self.__chassis

    def get_model(self) -> str:
        """
        This method is used to get the information of the vehicle' model.

        Returns:
        - str: the model of the vehicle
        """
        return self.__model

    def get_year(self) -> int:
        """
        This method is used to get the information of the vehicle' year.

        Returns:
        - int: the year of the vehicle
        """
        return self.__year

    def get_gas_consumption(self) -> float:
        """
        This method is used to get the information of the vehicle' gas consumption.

        Returns:
        - float: the gas consumption of the vehicle
        """
        return self.__gas_consumption

    def get_engine(self) -> Engine:
        """
        This method is used to get the information of the vehicle' engine.

        Returns:
        - Engine: the engine of the vehicle
        """
        return self.__engine

    def __str__(self):
        return f"Chassis: {self.__chassis}  Model: {self.__model}   Year: {self.__year}  \
             Consumption: {self.__gas_consumption}    Engine: {self.__engine}"


# ============================== SubClasses of Vehicles ==============================


class Car(Vehicle):
    """This class is a concrete definition for a Car."""

class Truck(Vehicle):
    """This class is a concrete definition for a truck."""


class Yacth(Vehicle):
    """This class is a concrete definition for a yatch."""

class Motorcycle(Vehicle):
    """This class is a concrete definition for a motorcycle."""
