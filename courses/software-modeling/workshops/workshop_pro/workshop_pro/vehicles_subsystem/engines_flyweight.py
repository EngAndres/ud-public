"""
This files contains the Flyweight implementation for the Engines Sub-system.
The idea is to reutilize the common engines across the vehicles.

Author: Carlos Sierra <cavirguezs@udistrital.edu.co>
"""

from ..engines_subsystem import Engine, EnginesFacade


# pylint: disable=too-few-public-methods
class EngineFlyweight:
    """
    This class represents the Flyweight for the Engines Sub-system.

    Attributes:
        __engines (dict): A dictionary with the engines.

    Methods:
        get_engine(Engine): This method returns an engine from the flyweight.
    """

    def __init__(self):
        self.__engines = {}

    def get_engine(self, engine_type: str, engine_price) -> Engine:
        """This method returns an engine from the flyweight."""
        if engine_type not in self.__engines:
            self.__engines[engine_type] = {}

        if engine_price not in self.__engines[engine_type]:
            self.__engines[engine_type][engine_price] = EnginesFacade.get_engine(
                engine_type, engine_price
            )

        return self.__engines[engine_type][engine_price]
