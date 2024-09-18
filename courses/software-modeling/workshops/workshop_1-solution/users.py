"""
This module has a class to define users in the context of 
the application.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>

This file is part of Workshop-SM-UD.

Workshop-SM-UD is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Workshop-SM-UD is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with Workshop-SM-UD. If not, see <https://www.gnu.org/licenses/>. 
"""

from abc import ABC, abstractmethod

# ========== User AbstractClass ========== #
class User(ABC):
    """This class represents the behavior of a general
    user in the application, ti acts as an abstract class."""

    def __init__(self, id_: int, name: str, email: str):
        self.__id = id_
        self.__name = name
        self.__email = email
        self.__grants = {}

    @abstractmethod
    def setup_grants(self):
        """This method defines the grants for an specific user."""

    def validate_grants(self, grant: str) -> bool:
        """This method validates if the user has an specific grant.

        In this method a grant is received as parameter in order
        to valide if the user has that grant or not in the application.

        Args:
            grant(str): A grant to be validated

        Returns:
            A boolean with the response of the requested grant.
        """
        return self.__grants[grant] if grant in self.__grants else False


# ========== Client Class ========== #
class Client(User):

    def __init__(self, id_: int, name: str, email: str, phone: str, address):
        super().__init__(id_, name, email)
        self.__phones = [phone]
        self.__addresses = [address]

    def setup_grants(self):
        self.__grants = {
            "add_videogames": False,
            "add_machine_material": False,
            "buy_machine": True,
        }
        
# ========== Manager Class ========== #
class Manager(User):

    def __init__(self, id_: int, name: str, email: str):
        super().__init__(id_, name, email)

    def setup_grants(self):
        self.__grants = {
            "add_videogames": True,
            "add_machine_material": True,
            "buy_machine": False,
        }
