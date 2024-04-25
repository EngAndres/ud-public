"""
This file contains the classes and methods to manage the videogames of the application.

Author: Carlo A. Sierra <cavirguezs@udistrital.edu.co>
"""

class VideoGame:
    """This class represents the behavior of a videogame"""

    def __init__(self, name: str, code: int, desription: str, price: float):
        self.name = name
        self.code = code
        self.desription = desription
        self.price = price
        self.new_launch = False
