"""
This file has some test classes related to the implementation of an Abstract Factory Pattern Design.

Author: Carlos Sierra <cavirguezs@udistrital.edu.co>
"""

from workshop_pro.engines_subsystem.factories import HighEngineFactory, LowEngineFactory
from workshop_pro.engines_subsystem.engines import ElectricEngine, GasEngine


class TestEngineFactories:
    """This class has different test cases to validate engines factories"""

    def setup_method(self):
        """
        This method is executed before each test method.
        """
        self.high_engine_factory = HighEngineFactory()
        self.low_engine_factory = LowEngineFactory()

    def test_create_high_electric_engine(self):
        """
        This method is a unit test for the create_electric_engine method
        of the HighEngineFactory class.
        """
        new_engine = self.high_engine_factory.create_electric_engine()
        assert isinstance(new_engine, ElectricEngine)

    def test_create_high_gas_engine(self):
        """
        This method is a unit test for the create_gas_engine method
        of the HighEngineFactory class.
        """

    def test_create_low_electric_engine(self):
        """
        This method is a unit test for the create_electric_engine method
        of the LowEngineFactory class.
        """

    def test_create_low_gas_engine(self):
        """
        This method is a unit test for the create_gas_engine method
        of the LowEngineFactory class.
        """
