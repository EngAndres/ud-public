"""
This module contains the Facade class that provides a simple interface 
to the complex logic of the Engines subsystem.

Author: Carlos Sierra <cavirguez@udistrital.edu.co>
"""

from .factories import HighEngineFactory, LowEngineFactory
from .engines import Engine


# pylint: disable=too-few-public-methods
class EnginesFacade:
    """
    This class is a Facade Pattern Design that provides a
    simple interface to the complex logic of the Engines subsystem.

    Methods:
        get_engine -> Engine: This method returns an engine object based on the type and price.
    """

    high_factory = HighEngineFactory()
    low_factory = LowEngineFactory()

    @staticmethod
    def get_engine(type_engine: str, price_engine: str) -> Engine:
        """
        This method returns an engine object based on the type and price.

        Args:
            type_engine (str): The type of the engine.
            price_engine (str): The price of the engine.

        Returns:
            An engine based on parameters.
        """
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
