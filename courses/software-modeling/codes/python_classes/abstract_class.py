"""
This is a module used to define an example of an abstract class.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>

=============================================
LICENCE - FOSS [Free Open Software Source]
"""

from abc import ABC, abstractmethod
from typing import Any

class AbstractClass(ABC):
    "   ""This class is a fingerprint for some concrete example classes."""

    # type-hint
    def __init__(self, parameter: Any):
        self.main_attr = parameter

    @abstractmethod
    def abstract_method(self):
        """This method is an abstract method."""


class ConcreteClass(AbstractClass):
    """This class is a concrete example of the abstract class."""

    def __init__(self, parameter: Any):
        super().__init__(parameter)

    def abstract_method(self):
        print(f"ConcreteClass: {self.main_attr}")


if __name__ == "__main__":
    concrete_object = ConcreteClass("Hello, World!")
    concrete_object.abstract_method()
    