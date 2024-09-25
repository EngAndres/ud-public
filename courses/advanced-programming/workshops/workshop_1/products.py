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

    def __init__(
        self,
        id_: str,
        name: str,
        brand: str,
        price: float,
        description: str,
        stock: int,
    ):
        self.__id = id_
        self.__name = name
        self.__brand = brand
        self.__price = price
        self.__description = description
        self.__stock = stock

    def is_id(self, id_: str) -> bool:
        """This method validates the id of the product.

        This method validates the id of the product
        and returns True if the id is the same as the
        id parameter or False if the id is different.

        Args:
            id_(str): id to be validated.

        Returns:
            A boolean value.
        """
        return True if id_ == self.__id else False

    def is_name(self, name: str) -> bool:
        """This method validates the name of the product.

        This method validates the name of the product
        and returns True if the name is the same as the
        name parameter or False if the name is different.

        Args:
            name(str): name to be validated.

        Returns:
            A boolean value.
        """
        return True if name in self.__name.lower() else False

    def is_brand(self, brand: str) -> bool:
        """This method validates the brand of the product.

        This method validates the brand of the product
        and returns True if the brand is the same as the
        brand parameter or False if the brand is different.    
    
        Args:
            brand(str): brand to be validated.
        
        Returns:
            A boolean value.
        """
        return True if brand in self.__brand.lower() else False

    
    def validate_stock(self) -> int:
        """This method validates the stock of the product.

        This method validates the stock of the product
        and returns True if the stock is greater than 0
        or False if the stock is 0.

        Returns:
            A boolean value.
        """
        return True if self.__stock > 0 else False

    def increase_stock(self, quantity: int):
        """This method increases the stock of the product.

        This method increases the stock of the product
        using the quantity as reference.

        Args:
            quantity(int): quantity to be added.
        """
        self.__stock += quantity

    def decrease_stock(self, quantity: int):
        """This method decreases the stock of the product.

        This method decreases the stock of the product
        using the quantity as reference.

        Args:
            quantity(int): quantity to be decreased.
        """
        if quantity <= self.__stock:
            self.__stock -= quantity
        else:
            print("Not enough stock.")

    def warning_stock(self, minimum_stock: int) -> str:
        """This method warns about the stock of the product.

        This method warns about the stock of the product
        using the minimum stock as reference.

        Args:
            minimum_stock(int): minimum stock to be warned.

        Returns:
            A string with the warning message.
        """
        if self.__stock < minimum_stock:
            return f"Warning: Electronic Device {self.__name} with\
                  ID {self.__id} has less than {minimum_stock} items.\n"
        return ""

    def __str__(self):
        return f"Name: {self.__name}\tPrice: {self.__price}\nDescription: {self.__description}\
                \t{'No Stock' if self.__stock == 0 else ''}"


# =============== Category Class ============= #
class Category:
    """This class represents the behavior of a category
    of electronic devices.

    Methods:
        get_name: returns the name of the category.
        add_product: adds a new product to the category.
        show_products: shows a list of products in the category.
        delete_product: deletes a product from the category.
        search_product_by_name: searches a product by name.
        search_product_by_brand: searches a product by brand.

    """

    def __init__(self, name: str):
        self.__name = name
        self.__products = []

    def get_name(self):
        """This method returns the name of the category."""
        return self.__name

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
        for i, product in enumerate(self.__products):
            print(f"Code: {i+1}, \n{product}")

    def get_product(self, index: int) -> ElectronicDevice:
        """This method returns a product from the category.

        This method returns a product from the category
        using the index as reference.

        Args:
            index(int): index of the product to be returned.

        Returns:
            A product object.
        """
        response = None
        if index < len(self.__products):
            response = self.__products[index]
        else:
            print("Invalid code.")
        return response

    def delete_product(self, product):
        """This method deletes a product from the category.

        This method deletes a product from the category
        using complete product object as reference.
        """
        self.__products.remove(product)

    def search_product_by_name(self, product_name: str) -> list:
        """This method searches some products in the category based on related name.

        This method searches a product in the category
        using the name of the product.

        Args:
            product_name(str): name of the product to be searched.

        Returns:
            A list with the products found.
        """
        temp_products = []
        for product in self.__products:
            if product_name in product.name.lower():
                temp_products.append(product)
        return temp_products

    def search_products_by_brand(self, brand_name: str) -> list:
        """This method searches some products in the category using the brand as filter.

        In this method a product is searched in the category
        using the brand name of the product.

        Args:
            brand_name(str): brand name of the product to be searched.

        Returns:
            A list with the products found.
        """
        temp_products = []
        for product in self.__products:
            if product.is_brand(brand_name.lower()):
                temp_products.append(product)
        return temp_products

    def search_products_with_stock(self) -> list:
        """This method searches some products in the category with stock.

        This method searches some products in the category making a valition
        about the stock of the product.

        Returns:
            A list with the products found.
        """
        temp_products = []
        for product in self.__products:
            if product.stock > 0:
                temp_products.append(product)
        return temp_products

    def warning_products(self, minimum_stock) -> str:
        """This method warns about the stock of the products in the category.

        This method warns about the stock of the products in the category
        using the minimum stock as reference.

        Args:
            minimum_stock(int): minimum stock to be warned.

        Returns:
            A string with the warning message for all products with less than
            minimum_stock value.
        """
        result = ""
        for product in self.__products:
            result += product.warning_stock(minimum_stock)
        return result
