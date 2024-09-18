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


class ElectronicDevice:
    """This class represents the behavior of an electronic
    device."""

    def __init__(self, id_: str, name: str, price: float, description: str, stock: int):
        self.id = id_
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock

    def __str__(self):
        return f"Name: {self.name}\tPrice: {self.price}\
                \t{'No Stock' if self.stock == 0 else ''}"


# =============== Category Class ============= #
class Category:
    """This class represents the behavior of a category
    of electronic devices."""

    def __init__(self):
        self.__products = []

    def add_product(self, product: ElectronicDevice):
        """This method adds a nee product to current category's defives.

        In this metthod a nre product is added to product lists.

        Args:
            product(ElectronicDevice): device to be added
        """

        self.__products.append(product)

    def show_products(self):
        """This method shows a list of products in the category.

        This method shows a list of products in the category
        with the following format:
        Name    Price    Observations
        """
        print("Name\tPrice\tObservations")
        for product in self.__products:
            print(product)

    def delete_product(self, product):
        """This method deletes a product from the category.

        This method deletes a product from the category
        using complete product object as reference.
        """
        self.__products.remove(product)
