"""
This module has a set of decorators in order to get performance
information about the system.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

import time
import resource
from typing import List

from .catalog_interface import Catalog
from ..observability_subsystem import Observability
from ..vehicles_subsystem import Vehicle


class TimePerformanceDecorator(Catalog):
    """
    This class is a decorator to get time performance information about the catalog functions.

    Methods:
        get_all_vehicles -> list: This method returns a list of all vehicles in the catalog.
        get_by_speed -> List[Vehicle]: This method returns a list of vehicles that have a speed
                                       between min_speed and max_speed.
        get_by_price -> List[Vehicle]: This method returns a list of vehicles that have a price
                                       between min_price and max_price.
        add_vehicle: This method adds a vehicle to the catalog.
        remove_vehicle: This method removes a vehicle from the catalog.
    """

    def __init__(self, catalog: Catalog):
        self.__catalog = catalog

    def get_all_vehicles(self) -> List[Vehicle]:
        start = time.time()
        result = self.__catalog.get_all_vehicles()
        end = time.time()
        Observability.write_performance_log(
            f"get_all_vehicles took {end - start} seconds"
        )
        return result

    def get_by_speed(self, min_speed: int, max_speed: int) -> List[Vehicle]:
        start = time.time()
        result = self.__catalog.get_by_speed(min_speed, max_speed)
        end = time.time()
        Observability.write_performance_log(f"get_by_speed took {end - start} seconds")
        return result

    def get_by_price(self, min_price: int, max_price: int) -> List[Vehicle]:
        start = time.time()
        result = self.__catalog.get_by_price(min_price, max_price)
        end = time.time()
        Observability.write_performance_log(f"get_by_price took {end - start} seconds")
        return result

    def add_vehicle(self, vehicle_type: str):
        start = time.time()
        self.__catalog.add_vehicle(vehicle_type)
        end = time.time()
        Observability.write_performance_log(f"add_vehicle took {end - start} seconds")

    def remove_vehicle(self, vehicle: Vehicle):
        start = time.time()
        self.__catalog.remove_vehicle(vehicle)
        end = time.time()
        Observability.write_performance_log(
            f"remove_vehicle took {end - start} seconds"
        )


class MemoryPerformanceDecorator(Catalog):
    """
    This class is a decorator to get memory performance information about the catalog functions.

    Methods:
        get_all_vehicles -> list: This method returns a list of all vehicles in the catalog.
        get_by_speed -> List[Vehicle]: This method returns a list of vehicles that have a speed
                                       between min_speed and max_speed.
        get_by_price -> List[Vehicle]: This method returns a list of vehicles that have a price
                                       between min_price and max_price.
        add_vehicle: This method adds a vehicle to the catalog.
        remove_vehicle: This method removes a vehicle from the catalog.
    """

    def __init__(self, catalog: Catalog):
        self.__catalog = catalog

    def get_all_vehicles(self) -> List[Vehicle]:
        start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.__catalog.get_all_vehicles()
        end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Observability.write_performance_log(f"get_all_vehicles took {end - start} Kb")

    def get_by_speed(self, min_speed: int, max_speed: int) -> List[Vehicle]:
        start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.__catalog.get_by_speed(min_speed, max_speed)
        end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Observability.write_performance_log(f"get_by_speed took {end - start} Kb")

    def get_by_price(self, min_price: int, max_price: int) -> List[Vehicle]:
        start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.__catalog.get_by_price(min_price, max_price)
        end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Observability.write_performance_log(f"get_by_price took {end - start} Kb")

    def add_vehicle(self, vehicle_type: str):
        start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.__catalog.add_vehicle(vehicle_type)
        end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Observability.write_performance_log(f"add_vehicle took {end - start} Kb")

    def remove_vehicle(self, vehicle: Vehicle):
        start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.__catalog.remove_vehicle(vehicle)
        end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Observability.write_performance_log(f"remove_vehicle took {end - start} Kb")
