"""
This file contains a Facade implementation for the Vehicles Sub-system.
The idea is to provide a simple interface to interact with the Vehicles Sub-system.

Author: Carlos Sierra <cavirguezs@udistrital.edu.co>
"""

from .engines_flyweight import EngineFlyweight
from .vehicle import Vehicle
from .vehicle_types import Helicopter, Scooter, Motorcycle, Car, Yacht, Truck


# pylint: disable=too-few-public-methods
class VehiclesFacade:
    """
    This class represents the Facade for the Vehicles Sub-system.

    Methods:
        create_vehicle -> Vehicle: This method creates a vehicle.
    """

    def __init__(self):
        self.__engine_flyweight = EngineFlyweight()

    def __get_vehicle_data(self) -> dict:
        """This method asks the user for the vehicle data."""
        data = {}
        data["vehicle_price"] = input("Enter the vehicle price: ")
        data["vehicle_model"] = input("Enter the vehicle model: ")
        data["vehicle_year"] = input("Enter the vehicle year: ")
        data["engine_chassis"] = input("Enter the engine chassis: ")
        return data

    def __get_car_data(self, data: dict) -> dict:
        """This method asks the user for the car data."""
        data["transmission"] = input("Enter the transmission: ")
        data["trade"] = input("Enter the trade: ")
        data["combustion_type"] = input("Enter the combustion type: ")
        return data

    def __get_yacht_data(self, data: dict) -> dict:
        """This method asks the user for the yacht data."""
        data["yacht_length"] = input("Enter the yacht length: ")
        data["yacht_width"] = input("Enter the yacht width: ")
        data["yacht_height"] = input("Enter the yacht height: ")
        return data

    def create_vehicle(self, vehicle_type) -> Vehicle:
        """This method creates a vehicle."""

        engine_type = input("Enter the engine type: ")
        engine_price = input("Enter the engine price: ")

        data = self.__get_vehicle_data()
        data["engine"] = self.__engine_flyweight.get_engine(engine_type, engine_price)

        if vehicle_type == "Helicopter":
            vehicle = Helicopter(
                data["chassis"],
                data["price"],
                data["engine"],
                data["model"],
                data["year"],
            )
        elif vehicle_type == "Scooter":
            vehicle = Scooter(
                data["chassis"],
                data["price"],
                data["engine"],
                data["model"],
                data["year"],
            )
        elif vehicle_type == "Motorcycle":
            vehicle = Motorcycle(
                data["chassis"],
                data["price"],
                data["engine"],
                data["model"],
                data["year"],
            )
        elif vehicle_type == "Car":
            data = self.__get_car_data(data)
            vehicle = Car(
                data["chassis"],
                data["price"],
                data["engine"],
                data["model"],
                data["year"],
                data["transmission"],
                data["trade"],
                data["combustion_type"],
            )
        elif vehicle_type == "Yacht":
            data = self.__get_yacht_data(data)
            vehicle = Yacht(
                data["chassis"],
                data["price"],
                data["engine"],
                data["model"],
                data["year"],
                data["length"],
                data["width"],
                data["height"],
            )
        elif vehicle_type == "Truck":
            vehicle = Truck(
                data["chassis"],
                data["price"],
                data["engine"],
                data["model"],
                data["year"],
            )
        else:
            raise ValueError("Invalid vehicle type.")

        return vehicle
