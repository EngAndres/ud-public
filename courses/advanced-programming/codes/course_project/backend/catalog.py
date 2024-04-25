"""
This file contains the classes and methods to manage the catalog of videogames of the application.

Author: Carlo A. Sierra <cavirguezs@udistrital.edu.co>
"""

class Catalog:
    """This class represents a catalog of videogames"""

    videogames = []

    @classmethod
    def show_catalog(cls):
        """
        This method is used to show the catalog of videogames.

        Returns:
            list: the list of videogames.
        """
        return cls.videogames

    @classmethod
    def show_by_category(cls, category: str):
        """
        This method is used to show the videogames by category.

        Args:
            category (str): the category of the videogames.
        
        Returns:
            A the list of videogames by category.
        """

        return [videogame for videogames if videogame.category == category]