"""
This module has a definition of an interface definition for Catalogs.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

from abc import ABC, abstractmethod
from typing import List

from ..vehicles_subsystem import Vehicle


class Catalog(ABC):
    """
    This is an interface for a catalog of vehicles.

    Methods:
        get_all_vehicles -> list: This method returns a list of all vehicles in the catalog.
        get_by_speed -> List[Vehicle]: This method returns a list of vehicles that have a speed
                                       between min_speed and max_speed.
        get_by_price -> List[Vehicle]: This method returns a list of vehicles that have a price
                                       between min_price and max_price.
        add_vehicle: This method adds a vehicle to the catalog.
        remove_vehicle: This method removes a vehicle from the catalog.
    """

    @abstractmethod
    def get_all_vehicles(self) -> List[Vehicle]:
        """
        This method returns a list of all vehicles in the catalog.
        """

    @abstractmethod
    def get_by_speed(self, min_speed: int, max_speed: int) -> List[Vehicle]:
        """
        This method returns a list of vehicles that have a speed between min_speed and max_speed.
        """

    @abstractmethod
    def get_by_price(self, min_price: int, max_price: int) -> List[Vehicle]:
        """
        This method returns a list of vehicles that have a price between min_price and max_price.
        """

    @abstractmethod
    def add_vehicle(self, vehicle_type: str):
        """
        This method adds a vehicle to the catalog.
        """

    @abstractmethod
    def remove_vehicle(self, vehicle: Vehicle):
        """
        This method removes a vehicle from the catalog.
        """
