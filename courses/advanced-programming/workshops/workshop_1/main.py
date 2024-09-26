"""
This module contains a set of classes to handle
electronic devices using categories, searchs, 
among others functionalities.

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

import sys
from client import AbstractUser, Client, Manager
from shopping_cart import ShoppingCart
from catalog import Catalog
from products import ElectronicDevice


class Main:
    """This class represents the main class of the application."""

    def __init__(self, user: AbstractUser):
        self.__user = user
        self.__catalog = Catalog()

        if isinstance(user, Client):
            self.__cart = ShoppingCart()

    def __show_menu_manager(self):
        """This function shows the menu for the manager."""
        menu = "1.Add category\n2.Show Categories\n\
            3.Remove Category\n4.Add product\n5.Show Warnings\n6.Exit\n"
        print(menu)

    def __show_menu_client(self):
        """This function shows the menu for the client."""
        menu = "1.Show Categories\n2.Show products by category\n\
            3.Search by name\n4.Search by brand\n\
            5.Search by category and stock\n6.Add product to cart\n\
            7.Show cart\n8.Clean cart\n9.Remove from cart\n10.Exit\n"
        print(menu)

    def show_menu(self):
        """This function shows the menu for the user."""
        if isinstance(self.__user, Manager):
            self.__show_menu_manager()
        elif isinstance(self.__user, Client):
            self.__show_menu_client()

    def __handle_manager(self, option: int) -> bool:
        exit_ = False
        if option == 1:
            category = input("Enter the category name: ")
            self.__catalog.add_category(category)
        elif option == 2:
            self.__catalog.show_categories()
        elif option == 3:
            category = input("Enter the category name: ")
            confirmation = input(
                f"Are you sure you want to delete {category} category? (y/n)"
            )
            if confirmation.lower() == "y":
                self.__catalog.remove_category(category)
        elif option == 4:
            category = input("Enter the category name: ")

            id_ = input("Enter the id of the product: ")
            name = input("Enter the name of the product: ")
            brand = input("Enter the brand of the product:")
            price = float(input("Enter the price of the product: "))
            description = input("Enter the description of the product: ")
            stock = int(input("Enter the initial stock of the product:"))
            product = ElectronicDevice(id_, name, brand, price, description, stock)

            self.__catalog.add_product_to_category(category, product)
        elif option == 5:
            minimum = int(input("Enter the minimum amount of stock to validate: "))
            self.__catalog.search_products_with_warning(minimum)
        elif option == 6:
            print("Thanks for using the application. Goodbye!")
            exit_ = True
        else:
            print("Invalid option. Please, read the menu and try again.")
        return exit_

    def __handle_client(self, option: int):
        exit_ = False
        if option == 1:  # show categories
            self.__catalog.show_categories()
        elif option == 2:  # show products by category
            category = input("Enter the category name: ")
            self.__catalog.show_products_by_category(category)
        elif option == 3:  # search by name
            name = input("Enter the name of the product: ")
            self.__catalog.search_product_by_name(name)
        elif option == 4:  # search by brand
            brand = input("Enter the brand of the product: ")
            self.__catalog.search_products_by_brand(brand)
        elif option == 5:  # search by category and stock
            category = input("Enter the category name: ")
            self.__catalog.search_products_by_category_with_stock(category)
        elif option == 6:  # add product to cart
            category = input("Enter the category name: ")
            product_code = int(input("Enter the product code: "))
            product = self.__catalog.get_product(category, product_code)
            self.__cart.add_product(product)
        elif option == 7:  # show cart
            self.__cart.show()
        elif option == 8:  # clean cart
            self.__cart.clean()
        elif option == 9:  # remove from cart
            id = None  # TODO get the right id without expose
            self.__cart.remove_product(id)
        elif option == 10:  # exit
            print("Thanks for using the application. Goodbye!")
            exit_ = True
        else:
            print("Invalid option. Please, read the menu and try again.")
        return exit_

    def handle_option(self, option: int) -> bool:
        """This function handles the option selected by the user.

        This function takes the option selected by the user and
        calls the corresponding method to handle the option.

        Args:
            option(int): option selected by the user.

        Returns:
            A boolean value to indicate if the user wants to exit the application.
        """
        if isinstance(self.__user, Manager):
            exit_ = self.__handle_manager(option)
        elif isinstance(self.__user, Client):
            exit_ = self.__handle_client(option)

        return exit_


# ========================= execute application ========================= #


def define_user():
    """This function defines the type of user in the application."""
    user_type = int(input("Enter the type of user: 1.Manage\n2.Client\n3.Exit"))
    user = None

    while user_type not in [1, 2, 3]:
        user_type = int(
            input(
                "Invalid option!\n\
                              Enter the type of user: 1.Manage\n2.Client\n3.Exit"
            )
        )

    if user_type == 1:
        user = Manager("Admin", "admin@udistrital.edu.co", "1990-01-01")
    elif user_type == 2:
        user = Client("Client", "client@udistrital.edu.co", "2009-01-01")
    elif user_type == 3:
        print("Goodbye!")
        sys.exit()
    return user


def run():
    """This function runs the application."""
    while True:
        user = define_user()
        app = Main(user)
        while True:
            app.show_menu()
            option = int(input("Enter an option: "))
            if app.handle_option(option):
                break


if __name__ == "__main__":
    run()
