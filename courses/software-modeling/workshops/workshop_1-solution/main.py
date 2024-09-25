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

import sys
import pickle
from datetime import datetime
from videogames import VideoGame
from machines import Machine
from users import User, Client, Manager, Address


# pylint: disable=too-few-public-methods
class Delivery:
    """This class represents the behavior of a delivery in the application."""

    def __init__(self, client_info: Client, address: Address, machine: Machine):
        self.__client_info = client_info
        self.__address = address
        self.__machine = machine

    def __str__(self) -> str:
        return f"{'='*10}\nClient: {self.__client_info}\n\
            Address: {self.__address}\nMachine: {self.__machine}"


class Main:
    """This class represents the main behavior of the application."""

    MENU_ADMIN = "1.Add Videogame\n2.Remove Videogame\n3.Exit"
    MENU_CLIENT = "1.Choose Material\n2.Show VideoGames\n3.Add VideoGame to Machine\4.Buy Machine\n5.Exit"

    def __init__(self, user: User):
        self.__catalog = []
        self.__temp_machine = None
        self.__user: User = user

    def change_user(self, user: User):
        """This method changes the current user."""
        self.__user = user

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

    def remove_videogame(self):
        """This method removes a videogame from the catalog.

        In this method based on videogame code, if the videogame
        exists it will be removed from current catalog.
        """
        if self.__user.validate_grants("remove_videogames"):
            success = False
            code = int(input("Insert the code of the videogame:"))
            response = self.__validate_videogame_code(code)
            if response is not None:
                self.__catalog.pop(response[0])
                success = True

            if success:
                print("Videogame removed successfully.")
            else:
                print(f"Videogame with code {code} is not in the catalog.")
        else:
            print("You do not have permission to remove a videogame.")

    def choose_material(self):
        """This method allows to choose the material of the machine."""
        if self.__user.validate_grants("buy_machine"):
            material = input(
                "Insert the material of the machine (wood, aluminum or carbon fiber):"
            )
            self.__temp_machine = Machine(material)
        else:
            print("You do not have permission to choose a material.")

    def add_videogame_to_machine(self):
        """This method adds a videogame to the machine."""
        if self.__user.validate_grants("buy_machine"):
            code = int(input("Insert the code of the videogame:"))
            response = self.__validate_videogame_code(code)
            if response is not None:
                self.__temp_machine.add_videogame(response[1])
                print("Videogame added successfully.")
            else:
                print("The videogame is not in the catalog.")
        else:
            print("You do not have permission to add a videogame.")

    def show_videogames(self):
        """This method shows all videogames in the catalog."""
        for vg in self.__catalog:
            print(vg)

    def __get_delivery_information(self):
        """This method gets the delivery information."""
        print("Choose delivery address:")
        for i, address in enumerate(self.__user.get_addresses()):
            print(f"{i+1}. {address}")
        option = int(input())
        temp_address = self.__user.get_addresses()[option - 1]
        delivery = Delivery(self.__user, temp_address, self.__temp_machine)

        file_name = f"delivery_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_\
            {self.__user.get_id()}.pkl"
        with open(file_name, "wb") as file:
            pickle.dump(delivery, file)

        print("Delivery will be sent to:", self.__user.get_addresses()[option - 1])

    def buy_machine(self):
        """This method buys the machine."""
        if isinstance(self.__user, Client) and (
            self.__user.validate_grant("buy_machine")
        ):
            if self.__temp_machine is not None:
                self.__get_delivery_information()
                self.__temp_machine = None
            else:
                print("You must choose a material first and add videogames.")
        else:
            print("You do not have permission to buy a machine.")

    def show_menu(self):
        """This method shows the menu according to the user type."""
        if isinstance(self.__user, Manager):
            print(Main.MENU_ADMIN)
        elif isinstance(self.__user, Client):
            print(Main.MENU_CLIENT)

    def __handle_admin(self, option: int):
        exit_ = False
        if option == 1:  # add videogame
            self.add_videogame()
        elif option == 2:  # remove videogame
            self.remove_videogame()
        elif option == 3:  # exit
            print("Manager view is closing!")
            exit_ = True

        return exit_

    def __handle_client(self, option: int) -> bool:
        exit_ = False
        if option == 1:  # choose material
            self.choose_material()
        elif option == 2:  # show videogames
            self.show_videogames()
        elif option == 3:  # add videogame to machine
            self.add_videogame_to_machine()
        elif option == 4:  # buy machine
            self.buy_machine()
        elif option == 5:  # exit
            print("Client view is closing!")
            exit_ = True

        return exit_

    def handle_option(self, option: int) -> bool:
        """This method handles the option selected by the user.

        Args:
            option (int): Option selected by the user.
        """
        if isinstance(self.__user, Manager):
            exit_ = self.__handle_admin(option)
        elif isinstance(self.__user, Client):
            exit_ = self.__handle_client(option)
        return exit_


# ======================= main execution ======================= #


def get_user() -> User:
    """This function gets the user type."""
    options = "1.Manager/n2.Client/n3.Exit"
    type_user = int(input(options))

    while type_user not in [1, 2, 3]:
        print("Invalid option. Please try again.")
        type_user = int(input(options))

    user = None
    if type_user == 1:
        user = Manager(1, "admin", "admin@udistrital.edu.co")
    elif type_user == 2:
        address = Address("St. Evergreen 123", 110783, "Springfield", "USA")
        user = Client(
            2, "client", "client@udistrital.edu.co", "+57 321 456789123", address
        )
    elif type_user == 3:
        print("Thanks for using the application. Goodbye!")
        sys.exit()

    return user


def run():
    """This function runs the application."""
    user = get_user()
    main = Main(user)

    while True:
        while True:
            main.show_menu()
            option = int(input("Enter the option:"))
            if main.handle_option(option):
                break

        user = get_user()
        main.change_user(user)


if __name__ == "__main__":
    run()
