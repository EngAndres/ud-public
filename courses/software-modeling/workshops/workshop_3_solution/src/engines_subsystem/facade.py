"""
This module contains the Facade class that provides a simple interface 
to the complex logic of the Engines subsystem.


"""
from .factories import HighEngineFactory, LowEngineFactory

class EnginesFacade():

    high_factory = HighEngineFactory()
    low_factory = LowEngineFactory()

    @staticmethod
    def get_engine(type_engine: str, price_engine: str):
        if price_engine == "high":
            if type_engine == "electric":
                engine = EnginesFacade().high_factory.create_electric_engine()
            else:
                engine = EnginesFacade().high_factory.create_gas_engine()
        elif price_engine == "low":
            if type_engine == "electric":
                engine = EnginesFacade().low_factory.create_electric_engine()
            else:
                engine = EnginesFacade().low_factory.create_gas_engine()
        else:
            raise ValueError("Invalid price value")

        return engine
        