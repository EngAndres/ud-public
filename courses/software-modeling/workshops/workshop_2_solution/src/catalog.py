"""
This file contains a Catalog class and an entry poiny menu
for vehicles catalog application.

Author: Carlos Sierra - cavirguezs@udistrital.edu.co
"""

from typing import List

from vehicles import Vehicle

class Catalog:

    def __init__(self):
        self.__vehicles = List[Vehicle]

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Catalog, cls).__new__(cls)
            cls.instance.vehicles = []
        return cls.instance

    def get_all_vehicles(self) -> List[Vehicle]:
        return self.__vehicles

    def get_price_by_range(self, min_price: float, max_price: float) -> List[Vehicle]:
        return [vehicle for vehicle in self.__vehicles if min_price <= vehicle.price <= max_price]

    def add_vehicle(self, vehicle: Vehicle):
        self.__vehicles.append(vehicle)
