"""
This module has a simple defition of a shopping card.

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

from products import ElectronicDevice


class ShoppingCart:
    """
    This class represents the behavior of a shopping cart.
    """

    def __init__(self):
        self.__products = []

    def add_product(self, product: ElectronicDevice):
        """This method adds a product to the shopping cart.

        This method takes an object of type ElectronicDevice and
        add into producs list.

        Args:
            product(ElectronicDevice): device to be added\\s
        """
        self.__products.append(product)

    def clean(self):
        """This method cleans the shopping cart.\w\
        """
        self.__products = []

    def calculate_total(self):
        """This method calculates the total price of the
        products in the sopping card.

        """
        cont = 0.0
        for product in self.__products:
            cont += product.price
        return cont

    def show(self):
        """This method shows the products in the shopping cart.

        This method shows all the products in the shopping cart
        and calculates the total price to be paid.
        """
        for product in self.__products:
            print(product)
        print(f"Total: {self.calculate_total()}")

    def remove_product(self, product_id: str):
        """This method removes a product from the shopping cart.

        This method takes a product id as reference and removes
        the product from the shopping cart.

        Args:
            product_id(str): id of the product to be removed.
        """
        for product in self.__products:
            if product.is_id(product_id):
                self.__products.remove(product)
                break