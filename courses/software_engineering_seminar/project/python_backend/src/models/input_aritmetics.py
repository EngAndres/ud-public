"""This module has a class to define some endpoints models.

Author: Carlos Andres Sierra <cavieguezs@udistrital.edu.co>
"""

from pydantic import BaseModel

class Input(BaseModel):
    """This class represents a typical input of two numbers
    to perfom any aritmetic number."""
    num_1: int
    num_2: int
