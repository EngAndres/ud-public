"""
This file contains the classes and methods to manage the videogames of the application.

Author: Carlos A. Sierra <cavirguezs@udistrital.edu.co>
"""

from pydantic import BaseModel

class VideoGame(BaseModel):
    """This class represents the behavior of a videogame"""

    name: str
    code: int
    description: str
    price: float
    new_launch: bool
