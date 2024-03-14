"""
This file contains a set of classes related with first course workshop.
This workshop is related to OOD and simple python classes definition.

Author: Carlos A. Sierra - Mar13/2024
"""


# ============================== Class Engine ==============================
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


# ============================== Class Vehicle ==============================
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
        return f"Chassis: {self.__chassis}  Model: {self.__model}   Year: {self.__year}   Consumption: {self.__gas_consumption}    Engine: {self.__engine}"


# ============================== Classes of Vehicles ==============================


class Car(Vehicle):
    """This class is a concrete definition for a Car."""

    def __init__(self, chassis, model, year, engine):
        super().__init__(chassis, model, year, engine)


class Truck(Vehicle):
    """This class is a concrete definition for a truck."""


class Yatch(Vehicle):
    """This class is a concrete definition for a yatch."""


class Motorcycle(Vehicle):
    """This class is a concrete definition for a motorcycle."""


# ============================== Menu ==============================

MESSAGE = """
    Please, choose an option:
    1. Create an engine
    2. Create a car
    3. Create a truck
    4. Create a yatch
    5. Create a motorcycle
    6. Show all engines
    7. Show all vehicles
    8. Exit
"""

enginees = {}
vehicles = []


def option_1():
    """This function lets create a new engine"""
    name = input("Please, write a name to identify the engine:")
    type_motor = input("Please, write the type of engine:")
    potency = int(input("Please, write the potency in a integer value for the engine:"))
    weight = float(input("Please, write the weight in a decimal value for the engine:"))
    new_engine = Engine(name, type_motor, potency, weight)
    enginees[name] = new_engine


def create_vehicle(vehicle_type: str):
    """
    This function lets create a new vehicle based on its type.

    Parameters:
    - vehicle_type (str): Vehicle type
    """

    engine_ = input(f"Please, write the name of the engine for the {vehicle_type}:")
    model = input(f"Please, write the model for the {vehicle_type}:")
    year = int(input(f"Please, write the year for the {vehicle_type}:"))
    chassis = input(f"Please, write the chassis (A or B) for the {vehicle_type}:")
    engine = enginees[engine_]
    if vehicle_type == "car":
        vehicles.append(Car(chassis, model, year, engine))
    elif vehicle_type == "truck":
        vehicles.append(Truck(chassis, model, year, engine))
    elif vehicle_type == "yatch":
        vehicles.append(Yatch(chassis, model, year, engine))
    elif vehicle_type == "motorcycle":
        vehicles.append(Motorcycle(chassis, model, year, engine))


def menu():
    """This function represents the menu of the application."""
    print(MESSAGE)
    option = int(input())
    while option != 8:
        if option == 1:
            option_1()
        elif option == 2:
            create_vehicle("car")
        elif option == 3:
            create_vehicle("truck")
        elif option == 4:
            create_vehicle("yatch")
        elif option == 5:
            create_vehicle("motorcycle")
        elif option == 6:
            print([str(engine) for engine in enginees.values()])
        elif option == 7:
            print([str(vehicle) for vehicle in vehicles])

        print(MESSAGE)
        option = int(input())


if __name__ == "__main__":
    menu()
