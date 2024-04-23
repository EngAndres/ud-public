"""
This file has some classes related to the implementation of an Abstract Factory Pattern Design..

Author: Carlos Sierra - cavirguez@udistrital.edu.co
"""

from abc import ABC

from engines import ElectricEngine, GasEngine


class AbstractEngineFactory(ABC):
    """This class is an abstract factory to create both gas and electric engines."""

    def create_electric_engine(self) -> ElectricEngine:
        """
        This method create an electric engine

        Returns:
        ElectricEngine: an electric engine object
        """

    def create_gas_engine(self) -> GasEngine:
        """
        This method create a gas engine.

        Returns:
        GasEngine: a gas engine object
        """


class HighEngineFactory(AbstractEngineFactory):
    """This class is a concrete factory to create expensive versions of engines"""

    def create_electric_engine(self) -> ElectricEngine:
        return ElectricEngine(
            torque=180,
            maximum_speed=300,
            dimenssions="200x200x200",
            power=200,
            stability="high",
            weight=100.9
        )

    def create_gas_engine(self) -> GasEngine:
        return GasEngine(
            torque=210,
            maximum_speed=400,
            dimenssions="210x200x250",
            power=250,
            stability="medium",
            weight=120.5
        )

class PoorEngineFactory(AbstractEngineFactory):
    """This class is a concrete factory to create cheap versions of engines"""

    def create_electric_engine(self) -> ElectricEngine:
        return ElectricEngine(
            torque=90,
            maximum_speed=100,
            dimenssions="100x100x100",
            power=50,
            stability="low",
            weight=63.4
        )

    def create_gas_engine(self) -> GasEngine:
        return GasEngine(
            torque=100,
            maximum_speed=150,
            dimenssions="110x100x150",
            power=100,
            stability="low",
            weight=80.5
        )
        