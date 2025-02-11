"""This module contains the interface for the Project DAOs.

Author: Carlos Andres Sierra <caviguezs@udistrital.edu.co>
"""

from abc import ABC
from pydantic import BaseModel


class ProjectDAO(ABC, BaseModel):
    """This class is the interface for the DAOs to be builded in the project context."""
