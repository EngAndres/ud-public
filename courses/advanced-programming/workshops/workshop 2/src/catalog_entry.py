"""
This file contains a class called CatalogEntry in order to handle authentications
and menu options.

Author: Carlos A. Sierra - Abr11/2024 <cavirguezs@udistrital.edu.co>
"""

from engines import Engine
from vehicles import Car, Truck, Yacth, Motorcycle

class CatalogEntry:
    """This class is a entry for catalog interaction"""

    def __init__(self):
        self.enginees = {}
        self.vehicles = []
        self.valid_users = {
            "professor": {
                "password": "admin",
                "role": "manager"
            },
            "student": {
                "password": "buyer",
                "role": "user"
            }
        }
        self.message_manager = """
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
        self.message_user = """
            Please, choose an option:
            1. Show all vehicles
            2. Exit
            """

    def create_engine(self):
        """This function lets create a new engine"""
        name = input("Please, write a name to identify the engine:")
        type_motor = input("Please, write the type of engine:")
        potency = int(input("Please, write the potency in a integer value for the engine:"))
        weight = float(input("Please, write the weight in a decimal value for the engine:"))
        new_engine = Engine(name, type_motor, potency, weight)
        self.enginees[name] = new_engine


    def create_vehicle(self, vehicle_type: str):
        """
        This function lets create a new vehicle based on its type.

        Parameters:
        - vehicle_type (str): Vehicle type
        """

        engine_ = input(f"Please, write the name of the engine for the {vehicle_type}:")
        model = input(f"Please, write the model for the {vehicle_type}:")
        year = int(input(f"Please, write the year for the {vehicle_type}:"))
        chassis = input(f"Please, write the chassis (A or B) for the {vehicle_type}:")
        engine = self.enginees[engine_]
        if vehicle_type == "car":
            self.vehicles.append(Car(chassis, model, year, engine))
        elif vehicle_type == "truck":
            self.vehicles.append(Truck(chassis, model, year, engine))
        elif vehicle_type == "yatch":
            self.vehicles.append(Yacth(chassis, model, year, engine))
        elif vehicle_type == "motorcycle":
            self.vehicles.append(Motorcycle(chassis, model, year, engine))

    def show_engines(self):
        """This method show all available engines"""
        print([str(engine) for engine in self.enginees.values()])

    def show_vehicles(self):
        """This method show all available vehicles"""
        print([str(vehicle) for vehicle in self.vehicles])

    def show_menu(self):
        """This function represents the menu of the application."""
        print(self.message_manager)
        option = int(input())
        while option != 8:
            if option == 1:
                self.create_engine()
            elif option == 2:
                self.create_vehicle("car")
            elif option == 3:
                self.create_vehicle("truck")
            elif option == 4:
                self.create_vehicle("yatch")
            elif option == 5:
                self.create_vehicle("motorcycle")
            elif option == 6:
                self.show_engines()
            elif option == 7:
                self.show_vehicles()

            print(self.message_manager)
            option = int(input())

    def validate_authentication(self, username: str, password: str) -> bool:
        """ 
        This method validates if a user has permissions to use the application.

        Parameters:
        - username (str): Username
        - password (str): username' password

        Returns:
        bool: access granted or not
        """
        if username in self.valid_users:
            if self.valid_users[username].get("password") == password:
                return True
        return False
