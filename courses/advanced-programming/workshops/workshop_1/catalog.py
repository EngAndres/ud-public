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

from products import Category, ElectronicDevice


class Catalog:
    """This class represents the behavior of a catalog of electronic devices.
    
    Methods:
        add_category: This method adds a new category to the catalog.
        remove_category: This method removes a category from the catalog.
        show_categories: This method shows the categories in the catalog.
        add_product_to_category: This method adds a product to a category.
        show_products_by_category: This method shows the products in a category.
        search_product_by_name: This method searches a product by name in the catalog.
        search_products_by_brand: This method searches a product by brand in the catalog.
        search_products_by_category_with_stock: This method searches products with stock in a category.
        search_products_with_warning: This method searches products with stock below a minimum.
    """

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

    def add_product_to_category(self, category: str, product: ElectronicDevice):
        """This method adds a product to a category.


        This method adds a product to a category using the
        add_product method of the Category class.

        Args:
            category(str): name of the category where the product will be added.
            product(ElectronicDevice): product to be added.
        """

        self.__categories[category].add_product(product)

    def show_products_by_category(self, category: str):
        """This method shows the products in a category.

        This method shows the products in a category using the
        show_products method of the Category class.
        """
        self.__categories[category].show_products()

    def get_product(self, category: str, product_code: int) -> ElectronicDevice:
        """This method gets a product from a category.

        This method gets a product from a category using the
        get_product method of the Category class.

        Args:
            category(str): name of the category where the product is.
            product_code(int): code of the product to be retrieved.

        Returns:
            An electronic device based on category and menu code.
        """
        return self.__categories[category].get_product(product_code - 1)

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

    def search_products_by_brand(self, brand_name: str):
        """This method searches a product by brand in the catalog.

        This method searches a product by brand in the catalog
        using the search_products_by_brand method of the Category class
        and showing the category and the products found.

        Args:
            brand_name(str): name of the brand to be searched.
        """
        for category, category_info in self.__categories.items():
            temp_products = category_info.search_products_by_brand(brand_name.lower())
            if len(temp_products) > 0:
                print(f"Category: {category}")
                for product in temp_products:
                    print("  - " + product)

    def search_products_by_category_with_stock(self, category: str):
        """This method searches products with stock in a category.

        This method searches products with stock in a category
        using the search_products_with_stock method of the Category class
        and showing the category and the products found.

        Args:
            category(str): name of the category to be searched.
        """
        temp_products = self.__categories[category].search_products_with_stock()
        if len(temp_products) > 0:
            print(f"Category: {category}")
            for product in temp_products:
                print("  - " + product)
        else:
            print(f"No products with stock in category {category}.")

    def search_products_with_warning(self, minimum_stock: int):
        """This method searches products with stock below a minimum.

        This method searches products with stock below a minimum
        using the warning_products method of the Category class
        and showing the category and the products found.

        Args:
            minimum_stock(int): minimum stock to be warned.
        """
        for category, category_info in self.__categories.items():
            temp_products = category_info.warning_products(minimum_stock)
            if temp_products != "":
                print(f"Category: {category}")
                print(temp_products)
