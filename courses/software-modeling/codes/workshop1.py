"""
This is a set of classes to get an answer for the workshop
number I of Software Design course.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""


class Engine:  
    """This class represents the behaviour of a vehicle motor"""

    def __init__(
        self, name_engine: str, type_engine: str, potency_engine: int, weight: float
    ):
        self.__name = name_engine
        self.__type_ = type_engine
        self.__potency = potency_engine
        self.__weight = weight

    def get_potency(self) -> int:
        """
        This method returns the potency of the engine.

        Returns:
        - int: potency of the engine
        """
        return self.__potency

    def get_weight(self) -> int:
        """
        This method returns the weight of the engine.

        Returns:
        - int: weight of the engine
        """
        return self.__weight

    def __str__(self):
        return f"Name: {self.__name}    Type: {self.__type_}    \
            Potency: {self.__potency}    Weight: {self.__weight}"


class Vehicle:  # pylint: disable=too-few-public-methods
    """This class is an abstraction of any vehicle"""

    def __init__(self, engine: Engine, chassis: str, model: str, year_car: int):
        self.__engine = engine
        self.__chasis = chassis
        self.__model = model
        self.__year = year_car
        self.__consumption = self.__calculate_gas_consupmtion()

    def get_engine(self) -> Engine:
        """
        This method returns the engine of the vehicle.

        Returns:
        - Engine: engine of the vehicle
        """
        return self.__engine

    def get_year(self) -> int:
        """
        This method returns the year of the vehicle.

        Returns:
        - int: year of the vehicle
        """
        return self.__year

    def __calculate_gas_consupmtion(self) -> float:
        """
        This method calculates consumption based on engine
        values.

        Returns:
        - float: vehicle consumption
        """
        consumption = (
            (1.1 * self.__engine.get_potency())
            + (0.2 * self.__engine.weight)
            + (0.3 if self.__chasis == "A" else 0.5)
        )
        return consumption

    def __str__(self):
        return f"Model: {self.__model}    Year: {self.__year}    Consumption: {self.__consumption}\
                Chassis: {self.__chasis}    Engine: {str(self.__engine)}"

class Car(Vehicle):  # pylint: disable=too-few-public-methods
    """This class represents the behevior of a Car vehicle"""


class Truck(Vehicle):  # pylint: disable=too-few-public-methods
    """This class represents the behavior of a Truck vehicle"""


class Yatch(Vehicle):  # pylint: disable=too-few-public-methods
    """This class represents the behavior of a Yatch vehicle"""


class Motorcycle(Vehicle):  # pylint: disable=too-few-public-methods
    """This class represents the behavior of a Motorcycle vehicle"""


# ==================================== MENU
MESSAGE = """
Option 1. Create engine
Option 2. Create car
Option 3. Create truck
Option 4. Create yatch
Option 5. Crear motorcyle
Option 6. Show engines
Option 7. Show vehicles
Option 8. Search by year
Option 9. Search by potency
Opcion 10. Exit
"""

# save data related to engines and vehicles in memory, sort of a database
engines = {}
vehicles = []


def create_engine():
    """This method lets add a new engine to list"""
    name_engine = input("Write engine name: ")
    type_engine = input("Write type of the engine: ")
    potency_engine = int(input("Write the potency of the engine: "))
    weight_engine = float(input("Write the weight of the engine: "))
    new_obj_engine = Engine(name_engine, type_engine, potency_engine, weight_engine)
    engines[name_engine] = new_obj_engine


def create_vehicle(type_vehicle: str):
    """
    This method lets create a new vehicle and add it to the
    catalog.

    Parameters:
    - type_vehicle (str): The type of the vehicle
    """
    chassis = input("Write the chassis of the vehicle (A or B):")
    if chassis not in ["A", "B"]:
        raise ValueError("Error: Chassis wrote is wrong. Must be A or B.")
    model = input("Write the model of the vehicle: ")
    year_ = int(
        input("Write the year of the vehicle (should be greater or equal than 2000): ")
    )
    if year_ < 2000:
        raise ValueError("Error. Year is not in a valid range.")
    engine_name = input("Write the name of the motor for the vehicle: ")

    try:
        engine = engines[engine_name]
        if type_vehicle == "car":
            vehicle_obj_new = Car(engine, chassis, model, year_)
        elif type_vehicle == "truck":
            vehicle_obj_new = Truck(engine, chassis, model, year_)
        elif type_vehicle == "yatch":
            vehicle_obj_new = Yatch(engine, chassis, model, year_)
        elif type_vehicle == "motorcycle":
            vehicle_obj_new = Motorcycle(engine, chassis, model, year_)
        vehicles.append(vehicle_obj_new)
    except Exception as e:
        print(f"Error: {e}.")


def search_by_year(year_: int) -> list:
    """
    This method makes a search of all vehicles of a specific
    year.

    Parameters:
    - year (int): Year to filter
    """
    return [vehicle for vehicle in vehicles if vehicle.get_year() == year_]


def search_by_potency(potency_: float) -> list:
    """
    This method makaes a search of vehicles based on the potency
    of the engine of the vehicle.

    Parameters:
    - potency_ (float): Potency to filter
    """
    return [vehicle for vehicle in vehicles if vehicle.get_engine().get_potency() == potency_]


print(MESSAGE)
option = int(input("Please, choise an option: "))
while option != 10:
    if option == 1:
        create_engine()
    elif option == 2:
        create_vehicle("car")
    elif option == 3:
        create_vehicle("truck")
    elif option == 4:
        create_vehicle("yatch")
    elif option == 5:
        create_vehicle("motorcycle")
    elif option == 6:
        for name, values in engines.items():
            print(f"{name} = {str(values)}")
    elif option == 7:
        for vehicle in vehicles:
            print(vehicle)
    elif option == 8:
        year = int(input("Please, write the year: "))
        search_by_year(year)
    elif option == 9:
        potency = float(input("Please, write the potency:"))
        search_by_potency(potency)
    else:
        print("Invalid option.")
    print("\n\n" + MESSAGE)
    option = int(input("Please, choise an option: "))
