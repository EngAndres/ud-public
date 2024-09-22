"""
This module has a class to define a general arcade videogames machine.

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

import pickle
from datetime import datetime
from videogames import VideoGame
from machines import Machine
from users import User, Client, Manager, Address

class Delivery:
    """This class represents the behavior of a delivery in the application."""

    def __init__(self, client_info: Client, address: Address, machine: Machine):
        self.__client_info = client_info
        self.__address = address
        self.__machine = machine

class Main:
    """This class represents the main behavior of the application."""

    USER_TYPE = "1.Client\n2.Admin\n3.Exit"
    MENU_ADMIN = "1.Add Videogame\n2.Remove Videogame\n3.Exit"
    MENU_CLIENT = (
        "1.Choose Material\n2.Show VideoGames\n3.Add VideoGame to Machine\4.Buy Machine\n5.Exit"
    )

    def __init__(self):
        self.__catalog = []
        self.__temp_machine = None
        self.__user : User = None

    def __validate_videogame_code(self, code: int) -> bool:
        """This method validates if a videogame code already exists in the catalog.

        In this method, the code of a videogame is received as argument,
        and it is validated if it already exists in the catalog.

        Args:
            code (int): Code of the videogame to be validated.
        """
        for i, vg in enumerate(self.__catalog):
            if vg.get_code() == code:
                return i, vg
        return None

    def add_videogame(self):
        """This method adds a videogame to the catalog."""
        if self.__user.validate_grants("add_videogame"):
            code = int(input("Insert the code of the videogame:"))
            while True:
                if self.__validate_videogame_code(code) is not None:
                    print("The code already exists, please insert a new one.")
                    code = int(input("Insert the code of the videogame:"))
                else:
                    break
            name = input("Insert the name of the videogame:")
            description = input("Insert the description of the videogame:")
            videogame = VideoGame(code, name, description)
            self.__catalog.append(videogame)
        else:
            print("You do not have permission to add a videogame.")

    def remove_videogame(self, code: int):
        """This method removes a videogame from the catalog.

        In this method based on videogame code, if the videogame
        exists it will be removed from current catalog.

        Args:
            code (int): Code of the videogame to be removed.
        """
        success = False
        response = self.__validate_videogame_code(code)
        if response is not None:
            self.__catalog.pop(response[0])
            success = True

        if success:
            print("Videogame removed successfully.")
        else:
            print(f"Videogame with code {code} is not in the catalog.")

    def choose_material(self):
        """This method allows to choose the material of the machine."""
        material = input("Insert the material of the machine (wood, aluminum or carbon fiber):")
        self.__temp_machine = Machine(material)

    def add_videogame_to_machine(self):
        """This method adds a videogame to the machine."""
        code = int(input("Insert the code of the videogame:"))
        response = self.__validate_videogame_code(code)
        if response is not None:
            self.__temp_machine.add_videogame(response[1])
            print("Videogame added successfully.")
        else:
            print("The videogame is not in the catalog.")

    def show_videogames(self):
        """This method shows all videogames in the catalog."""
        for vg in self.__catalog:
            print(vg)

    def get_delivery_information(self):
        """This method gets the delivery information."""
        print("Choose delivery address:")
        for i, address in enumerate(self.__user.get_addresses()):
            print(f"{i+1}. {address}")
        option = int(input())
        temp_address = self.__user.get_addresses()[option-1]
        delivery = Delivery(self.__user, temp_address, self.__temp_machine)

        file_name = f"delivery_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_\
            {self.__user.get_id()}.pkl"
        with open(file_name, 'wb') as file:
            pickle.dump(delivery, file)

        print("Delivery will be sent to:", self.__user.get_addresses()[option-1])

    def buy_machine(self):
        """This method buys the machine."""
        if self.__temp_machine is not None:
            if isinstance(self.__user, Client) and (self.__user.validate_grant("buy_machine")):
                self.get_delivery_information()
                self.__temp_machine = None
            else:
                print("You do not have permission to buy a machine.")
        else:
            print("You must choose a material first and add videogames.")
