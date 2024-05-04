"""
This is a file to test the Facade class of the Engines subsystem.

Author: Carlos Sierra <cavirguezs@udistrital.edu.co>
"""

import pytest

from workshop_pro.engines_subsystem.facade import EnginesFacade
from workshop_pro.engines_subsystem.engines import ElectricEngine, GasEngine


class TestEngineFacade:
    """This class contains the tests for the Facade class of the Engines subsystem."""

    @pytest.mark.parametrize("price", [("high"), ("low")])
    def test_electric(self, price):
        """
        This method is a unit test for the get_engine method
        with electric engines of the Facade class.
        """

        new_engine = EnginesFacade.get_engine("electric", price)
        assert isinstance(new_engine, ElectricEngine)

    @pytest.mark.parametrize("price", [("high"), ("low")])
    def test_gas(self, price):
        """
        This method is a unit test for the get_engine method
        with gas engines of the Facade class.
        """

        new_engine = EnginesFacade.get_engine("gas", price)
        assert isinstance(new_engine, GasEngine)
