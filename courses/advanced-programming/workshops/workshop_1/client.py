"""
This module contains a class to define the user in the application.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>

This file is part of Workshop_1_AP-UD.

Workshop_1_AP-UD is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Workshop_1_AP-UD is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with Workshop_1_AP-UD. If not, see <https://www.gnu.org/licenses/>. 
"""

from abc import ABC, abstractmethod
from datetime import datetime

# =============== Address Class ============= #
class Address: # abstract data type
    """This class represents the behavior of an address.
    """

    def __init__(self , street: str, city: str, country: str, zip_code: int):
        self.__street = street
        self.__city = city
        self.__country = country
        self.__zip_code = zip_code

    def set_zip_code(self, zip_code: int):
        """This method sets the zip code of the address.
        """
        self.__zip_code = zip_code

    def __str__(self):
        return f"Street: {self.__street}, {self.__city}, \
            {self.__country}, ZipCode: {self.__zip_code}"

# =============== AbstractUser Class ============= #
class AbstractUser(ABC):
    """
    This class represents the behavior of a user in the 
    application.
    """

    def __init__(self, name: str, email: str, birthday: str):
        self.name = name
        self.email = email
        self.__birthday = birthday
        self.__phones = []
        self.__grants = {}

    def add_phone(self, phone: str):
        """This method adds a phone to the user.
        """
        self.__phones.append(phone)

    def calculate_age(self):
        """This method calculates the age of the user.
        """
        return datetime.now().year - int(self.__birthday.split("-")[0])

    @abstractmethod
    def validate_grants(self, grant: str):
        """This method validates the grants of the user."""

# =============== Client Class ============= #
class Client(AbstractUser):
    """This class represents the behavior of a simple client."""

    def __init__(self, name: str, email: str, birthday: str)
        super().__init__(name, email, birthday)
        self.__address = []
        self.__create_grants()

    def add_address(self, street: str, city: str, country: str, zip_code: int):
        """This method adds an address to the client.
        """
        temp_address = Address(street, city, country, zip_code)
        self.__address.append(temp_address) 

    def __create_grants(self): 
        self.__grants = {
            "add_shopping_cart": True,
            "remove_shopping_cart": True,
            "show_shopping_cart": True,
            "add_categories": False,
            "add_products": False,           
        }

    def validate_grants(self, grant: str):
        """This method validates the grants of the user.
        """
        return self.__grants[grant] if grant in self.__grants else False


# =============== Manager Class ============= #
class Manager(AbstractUser):
    """This class represents the behavior of a manager."""

    def __init__(self, name: str, email: str, birthday: str):
        super().__init__(name, email, birthday)
        self.__create_grants()

    def __create_grants(self):
        self.__grants = {
            "add_shopping_cart": False,
            "remove_shopping_cart": False,
            "show_shopping_cart": False,
            "add_categories": True,
            "add_products": True,           
        }

    def validate_grants(self, grant: str):
        """This method validates the grants of the user.
        """
        return self.__grants[grant] if grant in self.__grants else False