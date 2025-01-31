"""This module is used to handle services related to videogames.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List
from pydantic import BaseModel
from repositories.videogames import VideoGameRepository, VideoGamesDAO


class NameCategoryDTO(BaseModel):
    """This is a data class to move data into the services"""

    name: str
    category: str


class VideoGameServices:
    """This class has the services for videogame searches."""

    def __init__(self):
        self.repository = VideoGameRepository()

    def get_all(self) -> List[VideoGamesDAO]:
        """This method is used to get all videogames.

        Returns:
            A list of videogames.
        """
        return self.repository.get_videogames()

    def get_by_name(self, name: str) -> List[VideoGamesDAO]:
        """This method is used to get videogames by name.

        Args:
            name (str): The name of the videogame.

        Returns:
            A list of videogames with the name.
        """
        response = []
        for videogame in self.repository.get_videogames():
            if name.lower() in videogame.name.lower():
                response.append(videogame)
        return response

    def get_by_category(self, category: str) -> List[VideoGamesDAO]:
        """This method is used to get videogames by category.

        Args:
            category (str): The category of the videogame.

        Returns:
            A list of videogames with the category.
        """
        response = []
        for videogame in self.repository.get_videogames():
            if category.lower() in videogame.category.lower():
                response.append(videogame)
        return response

    def get_by_price(self, min_price: float, max_price: float) -> List[VideoGamesDAO]:
        """This method is used to get videogames by price.

        Args:
            min_price (float): The minimum price of the videogame.
            max_price (float): The maximum price of the videogame.

        Returns:
            A list of videogames with the price.
        """
        response = []
        for videogame in self.repository.get_videogames():
            if min_price <= videogame.price <= max_price:
                response.append(videogame)
        return response

    def get_by_description(self, keyword: str) -> List[VideoGamesDAO]:
        """This method is used to get videogames by description.

        Args:
            keyword (str): The keyword to be searched in the description of the videogame.

        Returns:
            A list of videogames with the description.
        """
        response = []
        for videogame in self.repository.get_videogames():
            if keyword.lower() in videogame.description.lower():
                response.append(videogame)
        return response

    def get_by_name_category(
        self, name_category: NameCategoryDTO
    ) -> List[VideoGamesDAO]:
        """This method is used to get videogames by name and category.

        Args:
            name_category (NameCategoryDTO): The name and category of the videogame.

        Returns:
            A list of videogames with the name and category.
        """
        response = []
        for videogame in self.repository.get_videogames():
            if (
                name_category.name.lower() in videogame.name.lower()
                and name_category.category.lower() in videogame.category.lower()
            ):
                response.append(videogame)
        return response
