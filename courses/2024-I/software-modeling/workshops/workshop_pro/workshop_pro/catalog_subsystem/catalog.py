"""
This module has a definition of both an interface and a concrete definition for Catalogs.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List

from .catalog_interface import Catalog
from ..vehicles_subsystem import Vehicle, VehiclesFacade


class CatalogConcrete(Catalog):
    """
    This is a concrete implementation of the Catalog interface.

    Methods:
        get_all_vehicles -> list: This method returns a list of all vehicles in the catalog.
        get_by_speed -> List[Vehicle]: This method returns a list of vehicles that have a speed
                                       between min_speed and max_speed.
        get_by_price -> List[Vehicle]: This method returns a list of vehicles that have a price
                                       between min_price and max_price.
        add_vehicle: This method adds a vehicle to the catalog.
        remove_vehicle: This method removes a vehicle from the catalog.
    """

    def __init__(self):
        self.__vehicles = []
        self.__vehicles_facade = VehiclesFacade()

    def get_all_vehicles(self) -> List[Vehicle]:
        return self.__vehicles

    def get_by_speed(self, min_speed: int, max_speed: int) -> List[Vehicle]:
        return [
            vehicle
            for vehicle in self.__vehicles
            if vehicle.is_in_speed(min_speed, max_speed)
        ]

    def get_by_price(self, min_price: int, max_price: int) -> List[Vehicle]:
        return [
            vehicle
            for vehicle in self.__vehicles
            if vehicle.is_in_price(min_price, max_price)
        ]

    def add_vehicle(self, vehicle_type: str):
        self.__vehicles.append(self.__vehicles_facade.create_vehicle(vehicle_type))

    def remove_vehicle(self, vehicle: Vehicle):
        self.__vehicles.remove(vehicle)
