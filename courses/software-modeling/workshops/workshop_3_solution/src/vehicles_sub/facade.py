from .vehicles import Vehicle
from .flyweight import EngineFlyweight


from abc import ABC


class VehicleFacade(ABC):
    vehicle = Vehicle()
    engine_flyweight = EngineFlyweight()

    @staticmethod
    def create_vehicle(type_vehicle: str, **kwargs) -> Vehicle:
        engine = VehicleFacade().engine_flyweight.create_engine(
            kwargs.get("type_engine"), kwargs.get("price_engine")
        )
        kwargs["engine"] = engine
        vehicle = VehicleFacade().vehicle.get_vehicle(type_vehicle, **kwargs)
        return vehicle
