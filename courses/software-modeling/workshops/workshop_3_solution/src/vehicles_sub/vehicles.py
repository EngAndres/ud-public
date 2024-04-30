"""
This file has a set of classes related to vehicles,
including of the all subtypes of vehicles.


Author: Carlos Sierra - cavirguez@udistrital.edu.co
"""

from abc import ABC

# pylint: disable=too-few-public-methods
class Vehicle(ABC):
    """This class represents an abstraction of a vehicle inside the catalog business model."""

    def __init__(self, **kwargs):
        self.engine = kwargs.get("engine")
        self.chassis = kwargs.get("chassis")
        self.price = kwargs.get("price")
        self.model = kwargs.get("model")
        self.year = kwargs.get("year")

    def get_vehicle(self, type_vehicle: str, **kwargs) -> __class__:
        if type_vehicle == "helicopter":
            return Helicopter(**kwargs)
        elif type_vehicle == "scooter":
            return Scooter(**kwargs)
        elif type_vehicle == "motorcycle":
            return Motorcycle(**kwargs)
        elif type_vehicle == "car":
            return Car(**kwargs)
        elif type_vehicle == "truck":
            return Truck(**kwargs)
        elif type_vehicle == "yacht":
            return Yacht(**kwargs)
        else:
            raise ValueError("Invalid vehicle type")

    def _basic_info(self):
        return f"Model: {self.model} - Year: {self.year} - Price: {self.price} - \
             Engine: {self.engine} - Chassis: {self.chassis}"

    def __str__(self) -> str:
        return self._basic_info()


class Helicopter(Vehicle):
    """This class is a concrete implementation of an helicopter"""


class Scooter(Vehicle):
    """This class is a concrete implementation of a scoorter"""


class Motorcycle(Vehicle):
    """This class is a concrete implementation of a motorcycle"""


class Car(Vehicle):
    """This class is a concrete implementation of a car"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transmission = kwargs.get("transmission")
        self.trade = kwargs.get("trade")
        self.combustible_type = kwargs.get("combustible_type")

    def __str__(self) -> str:
        return f"{super().__str__()} - Transmission: {self.transmission} - \
            Trade: {self.trade} - Combustible Type: {self.combustible_type}"


class Truck(Vehicle):
    """This class is a concrete implemtantion of a truck"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.consumption = self.__calculate_gas_consupmtion()


    def __calculate_gas_consupmtion(self) -> float:
        """
        This method calculates consumption based on engine
        values.

        Returns:
        - float: vehicle consumption
        """
        consumption = (
            (1.1 * self.engine.power)
            + (0.2 * self.engine.weight)
            + (0.3 if self.chassis == "A" else 0.5)
        )
        return consumption

    def __str__(self) -> str:
        return f"{super().__str__()} - Consumption: {self.consumption}"


class Yacht(Vehicle):
    """This class is a concrete implementation of a yatch"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = kwargs.get("length")
        self.weight = kwargs.get("weight")
        self.trade = kwargs.get("trade")

    def __str__(self) -> str:
        return f"{super().__str__()} - Length: {self.length} - \
            Weight: {self.weight} - Trade: {self.trade}"
