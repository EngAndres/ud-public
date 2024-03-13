"""
This file contains a set of classes related with first course workshop.
This workshop is related to OOD and simple python classes definition.

Author: Carlos A. Sierra - Mar13/2024
"""

# ============================== Class Engine ==============================
class Engine:  # pylint: disable=too-few-public-methods
    """This class represents the behavior of a vehicle engine."""

    def __init__(self, name, type_motor: str, potency: int, weight: float):
        self.name = name
        self.type_ = type_motor
        self.potency = potency
        self.weight = weight

# ============================== Class Vehicle ==============================
class Vehicle:
    """
    This class represents the behavior of an abstract class
    to define vehicles.
    """

    def __init__(self, chassis: str, model: str, year: int, engine: Engine):
        if not chassis in ["A", "B"]:
            raise ValueError("This chassis is not valid.")
        if year < 1990:
            raise ValueError("The year is not ina valid range.")
        self.__chassis = chassis
        self.__model = model
        self.__year = year
        self.__gas_consumption = None
        self.__engine = engine

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

global message = """
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

global enginees = {}
global vehicles = []

def option_1():
    name = input("Please, write a name to identify the engine:")
    type_motor = input("Please, write the type of engine:")
    potency = int(input("Please, write the potency in a integer value for the engine:"))
    weight = float(input("Please, write the weight in a decimal value for the engine:"))
    new_engine = Engine(type_motor, potency, weight)
    enginees.[name] = new_engine

def create_vehicle(vehicle_type: str):
    engine = input(f"Please, write the name of the engine for the {vehicle_type}:")
    model = input(f"Please, write the model for the {vehicle_type}:")
    year = int(input(f"Please, write the year for the {vechicle_type}:"))
    chassis = input(f"Please, write the chassis (A or B) for the {vechicle_type}:")
    if vehicle_type == "car":
        vehicles.append( Car(chassis, model, year, engine) )
    elif vehicle_type == "truck":

def menu():
    """This function represents the menu of the application."""
    print(message)
    option = int(input())
    while option != 8:
        if option == 1:
            option_1()
        else option == 2:
            create_vehicle("car")
        elif option == 3:
            create_vehicle("truck")
        elif option == 4:
            create_vehicle("yatch")
        elif option == 5:
            create_vehicle("motorcycle")
        elif option == 6:
            print(enginees)
        elif option == 7:
            print(vehicles)




if __name__ == "__main__":
    menu()
