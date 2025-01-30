"""This module is used to handle data related to videogames.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>"""

import json
from typing import List
from pydantic import BaseModel
from environment_variables import EnvironmentVariables

class VideoGamesDAO(BaseModel):
    """This class is used to define data structure related to videogames."""
    name: str
    category: str 
    price: float
    description: str
    
class VideoGameRepository:
    
    def __init__(self):
        """This method is used to initialize the class."""
        path_file = EnvironmentVariables().path_videogames_data
        self._load_data(path_file)

    def _load_data(self, path_file: str):
        try:
            with open(path_file, "r",encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print("File not found")
            self.data = []
                
    def get_videogames(self) -> List[VideoGamesDAO]:
        """This method is used to get all videogames."""
        videogames = []
        for videogame in self.data:
            videogame_temp = VideoGamesDAO(
                name = videogame["name"],
                category = videogame["category"],
                price = videogame["price"],
                description = videogame["description"]
            )
            videogames.append(videogame_temp)
        return videogames
