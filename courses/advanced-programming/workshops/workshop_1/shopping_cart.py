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

class ShoppingCart:
    """
    This class represents the behavior of a shopping cart.
    """
    
    def __init__(self):
        self.products = None

    def add_product(self, product: ElectronicDevice):
        self.products.append(product)
    
    def clean(self):
        self.products = None

    def calculate_total(self):
        """This method calculates the total price of the
        products in the sopping card"""
        cont = 0.0
        for product in list(self.products):
            cont += product.price
        return cont