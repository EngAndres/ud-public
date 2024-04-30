from abc import ABC

class CatalogInterface(ABC):
    
    def add_vehicle(self, **kwargs):
        pass

    def get_all_vehicles(self):
        pass

    def get_price_by_range(self, min_price: float, max_price: float):
        pass

    def get_by_speed(self, max_speed: float):
        pass

    def update_vehicle(self, model, **kwargs):
        pass

    def delete_vehicle(self, model):
        pass
    