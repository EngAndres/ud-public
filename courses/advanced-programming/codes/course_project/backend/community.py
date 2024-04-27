"""This fila saves information related to community management"""

from typing import List
from pydantic import BaseModel
from .users import Player

class Community(BaseModel):
    """This class represents the behavior of a videogames community"""

    name: str
    creater: Player
    members: List[Player]
