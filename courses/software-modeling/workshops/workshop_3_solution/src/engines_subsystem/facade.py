"""
This module contains the Facade class that provides a simple interface 
to the complex logic of the Engines subsystem.


"""
from . import factories

class EnginesFacade():

    high_factory = factories.HighEngineFactory()
    low_factory = factories.LowEngineFactory()

    @staticmethod
    def get_engine(type_engine: str, price_engine: str):
        if price_engine == "high":
            if type_engine == "electric":
                return EnginesFacade().high_factory.create_electric_engine()
            else:
                return EnginesFacade().high_factory.create_gas_engine()
        elif price_engine == "low":
            if type_engine == "electric":
                return EnginesFacade().low_factory.create_electric_engine()
            else:
                return EnginesFacade().low_factory.create_gas_engine()
        else:
            raise ValueError("Invalid price value")

if __name__ == "__main__":
    high_gas = EnginesFacade.get_engine("gas", "high")
    low_electric = EnginesFacade.get_engine("electric", "low")

    print(high_gas)
    print(low_electric)
