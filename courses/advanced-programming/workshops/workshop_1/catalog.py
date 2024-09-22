"""
This module contains a class to handle a catalog including some 
search methods.

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

from products import Category


class Catalog:
    """This class represents the behavior of a catalog of electronic devices."""

    def __init__(self):
        self.__categories = {}

    def add_category(self, category_name: str):
        """This method adds a new category to the catalog.

        In this method a category name is used to create a key
        in the dictionary where categories are stored and
        a new empty category is created.

        Args:
            category_name(str): name of the category to be added.
        """
        if category_name not in self.__categories:
            self.__categories[category_name] = Category(category_name)
            print(f"Category {category_name} added successfully.")
        else:
            print(f"Category {category_name} already exists.")

    def remove_category(self, category_name: str):
        """This method removes a category from the catalog.

        In this method a category is removed from the catalog
        using the category name as key.

        Args:
            category_name(str): name of the category to be removed.
        """
        del self.__categories[category_name]

    def show_categories(self):
        """This method shows the categories in the catalog.

        This method shows the categories based on the keys of
        the dictionary where categories are stored.
        """
        categories = list(self.__categories.keys())
        print(f"Categories: {categories}")

    def show_products_by_category(self, category: str):
        """This method shows the products in a category.

        This method shows the products in a category using the
        show_products method of the Category class.
        """
        self.__categories[category].show_products()

    def search_product_by_name(self, product_name: str):
        """This method searches a product by name in the catalog.
        
        This method searches a product by name in the catalog
        using the search_product method of the Category class
        and showing the category and the products found.

        Args:
            product_name(str): name of the product to be searched.W
        """
        for category, category_info in self.__categories.items():
            temp_products = category_info.search_product_by_name(product_name.lower())
            if len(temp_products) > 0:
                print(f"Category: {category}")
                for product in temp_products:
                    print("  - " + product)
