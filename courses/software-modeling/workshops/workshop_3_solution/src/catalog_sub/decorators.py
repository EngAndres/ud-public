from .catalog_interface import CatalogInterface
from ..observability_sub import Observability


class MemoryPerformanceDecorator(CatalogInterface):
    """This class represents the behavior of a catalog with memory performance"""

    def __init__(self, catalog: CatalogInterface):
        self.__catalog = catalog

    def get_all_vehicles(self):
        results = self.__catalog.get_all_vehicles()
        return results

    def get_price_by_range(self, min_price: float, max_price: float):
        results = self.__catalog.get_price_by_range(min_price, max_price)
        return results

    def get_by_speed(self, max_speed: float):
        results = self.__catalog.get_by_speed(max_speed)
        return results

    def add_vehicle(self, **kwargs):
        return self.__catalog.add_vehicle(**kwargs)

    def update_vehicle(self, model, **kwargs):
        return self.__catalog.update_vehicle(model, **kwargs)

    def delete_vehicle(self, model):
        return self.__catalog.delete_vehicle(model)


class TimePerformanceDecorator(CatalogInterface):
    """This class represents the behavior of a catalog with time performance"""

    def __init__(self, catalog: CatalogInterface):
        self.__catalog = catalog

    def get_all_vehicles(self):
        results = self.__catalog.get_all_vehicles()
        return results

    def get_price_by_range(self, min_price: float, max_price: float):
        results = self.__catalog.get_price_by_range(min_price, max_price)
        return results

    def get_by_speed(self, max_speed: float):
        results = self.__catalog.get_by_speed(max_speed)
        return results

    def add_vehicle(self, **kwargs):
        return self.__catalog.add_vehicle(**kwargs)

    def update_vehicle(self, model, **kwargs):
        return self.__catalog.update_vehicle(model, **kwargs)

    def delete_vehicle(self, model):
        return self.__catalog.delete_vehicle(model)
