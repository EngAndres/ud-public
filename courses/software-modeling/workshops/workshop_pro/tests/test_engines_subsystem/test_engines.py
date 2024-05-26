"""
This file has some test cases related to engines creation.

Author: Carlos Sierra <cavirguezs@udistrital.edu.co>
"""

from workshop_pro.engines_subsystem.engines import Engine, GasEngine, ElectricEngine


# pylint: disable=attribute-defined-outside-init
class TestEngine:
    """This class tests the Engine class"""

    @classmethod
    def setup_class(cls):
        """This is a method to create dummy data for engines creation"""
        cls.data_test = {
            "torque": 100,
            "maximum_speed": 200,
            "dimenssions": "100x100x100",
            "power": 150,
            "stability": "medium",
            "weight": 100.5,
        }

    def test_create_engine(self):
        """This is a test case to verify the creation of a base engine"""
        new_engine = Engine(
            torque=self.data_test["torque"],
            maximum_speed=self.data_test["maximum_speed"],
            dimenssions=self.data_test["dimenssions"],
            power=self.data_test["power"],
            stability=self.data_test["stability"],
            weight=self.data_test["weight"],
        )
        torque = self.data_test.get("torque")
        maximum_speed = self.data_test["maximum_speed"]
        dimenssions = self.data_test["dimenssions"]
        power = self.data_test["power"]
        stability = self.data_test["stability"]
        weight = self.data_test["weight"]

        assert (
            str(new_engine)
            == f"Engine: torque={torque}, \
                maximum_speed={maximum_speed}, \
                dimenssions={dimenssions}, \
                power={power}, \
                stability={stability}, \
                weight={weight}"
        )

    def test_liskov_gas_engine(self):
        """This is a test case to verify the creation of a gas engine"""
        new_gas_engine = GasEngine(
            torque=self.data_test["torque"],
            maximum_speed=self.data_test["maximum_speed"],
            dimenssions=self.data_test["dimenssions"],
            power=self.data_test["power"],
            stability=self.data_test["stability"],
            weight=self.data_test["weight"],
        )

        assert isinstance(new_gas_engine, GasEngine)
        assert isinstance(new_gas_engine, Engine)

    def test_liskov_electric_engine(self):
        """This is a test case to verify the creation of an electric engine"""
        new_electric_engine = ElectricEngine(
            torque=self.data_test["torque"],
            maximum_speed=self.data_test["maximum_speed"],
            dimenssions=self.data_test["dimenssions"],
            power=self.data_test["power"],
            stability=self.data_test["stability"],
            weight=self.data_test["weight"],
        )

        assert isinstance(new_electric_engine, ElectricEngine)
        assert isinstance(new_electric_engine, Engine)
