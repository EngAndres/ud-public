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


# ========== Address Class ========== #
class Address:  # abstract data type
    """This class represents the behavior of an address in the application."""

    def __init__(
        self, street: str, zip_code: int, city: str, country: str = "Colombia"
    ):
        self.__street = street
        self.__zip_code = zip_code
        self.__city = city
        self.__country = country

    def __str__(self) -> str:
        return f"{'='*10}\nStreet: {self.__street}\nZip Code: {self.__zip_code}\n\
            City: {self.__city}\nCountry: {self.__country}"


# ========== User AbstractClass ========== #
class User(ABC):
    """This class represents the behavior of a general
    user in the application, ti acts as an abstract class."""

    def __init__(self, id_: int, name: str, email: str):
        self._id = id_
        self._name = name
        self._email = email
        self._grants = {}

    def get_id(self) -> int:
        """This method returns the id of the user.

        Returns:
            An integer with the id of the user.
        """
        return self._id

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
        return self._grants[grant] if grant in self._grants else False


# ========== Client Class ========== #
class Client(User):
    """This class represents the behavior of a general client in the application."""

    def __init__(self, id_: int, name: str, email: str, phone: str, address: Address):
        super().__init__(id_, name, email)
        self.__phones = [phone]
        self.__addresses = [address]

    def setup_grants(self):
        self._grants = {
            "add_videogames": False,
            "remove_videogames": False,
            "add_machine_material": False,
            "buy_machine": True,
        }

    def add_phone(self, phone: str):
        """This method adds an additional phone number to the client.

        In this method a phone in string format is taken and added at the
        end of the list of user's phones.

        Args:
            phone (str): Phone number to be added.
        """
        self.__phones.append(phone)

    def add_address(
        self, street: str, zip_code: int, city: str, country: str = "Colombia"
    ):
        """This method adds an additional address to the client.

        In this method an address is created and added at the end of the
        list of user's addresses.

        Args:
            street (str): Street of the address.
            zip_code (int): Zip code of the address.
            city (str): City of the address.
            country (str): Country of the address.
        """
        address_temp = Address(street, zip_code, city, country)
        self.__addresses.append(address_temp)

    def get_addresses(self) -> list:
        """This method returns the list of addresses of the client.

        Returns:
            A list with the addresses of the client.
        """
        return self.__addresses

    def __str__(self):
        return f"Name: {self._name}\nEmail: {self._email}\nPhones:{' --- '.join(self.__phones)}"

# ========== Manager Class ========== #
class Manager(User):
    """This class represents the behavior of a general manager in the application."""

    def __init__(self, id_: int, name: str, email: str):
        super().__init__(id_, name, email)

    def setup_grants(self):
        self._grants = {
            "add_videogames": True,
            "remove_videogames": True,
            "add_machine_material": True,
            "buy_machine": False,
        }
