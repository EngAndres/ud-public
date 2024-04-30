"""
This file contains the classes and methods to manage the catalog of videogames of the application.

Author: Carlo A. Sierra <cavirguezs@udistrital.edu.co>
"""

from .videogames import VideoGame

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

        return [videogame for videogame in cls.videogames if videogame.category == category]

    @classmethod
    def show_new_launches(cls):
        """This method shows all videogames marked as new launches"""
        return [videogame for videogame in cls.videogames if videogame.new_launch]

    @classmethod
    def show_categories(cls):
        """This method shows all distinct categories in videogames"""
        categories = []
        for videogame in cls.videogames:
            if videogame.category not in categories:
                categories.append(videogame.category)
        return categories

    @classmethod
    def add_videogame(cls,  videogame: VideoGame):
        """
        This  method adds a videogame to catalog list.

        Args:
            videogame (VideoGame): videogame object to add
        """
        cls.videogames.append(videogame)


    @classmethod
    def update_videogame(cls, code: int, videogame: VideoGame):
        """This method updates avideogame in the list based on its code.
        """
        for i in range(len(cls.videogames)):
            if cls.videogames[i].code == code:
                cls.videogames[i] = videogame
                break

    @classmethod
    def get_videogame(cls, code: int) -> VideoGame:
        """This method performs asearch by code"""
        for videogame in cls.videogames:
            if videogame.code == code:
                return videogame
        return None
