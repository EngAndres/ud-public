"""
This module has a class to define a simple videogame.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>

This file is part of Workshop-SM-UD.

Workshop-SM-UD is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Workshop-SM-UD is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with Workshop-SM-UD. If not, see <https://www.gnu.org/licenses/>. 
"""

class VideoGame:
    """This class represents the behavior of a general videogame."""

    def __init__(self, code: int, name: str, description: str):
        self.__code = code
        self.__name = name
        self.__description = description

    def get_code(self) -> int:
        """This method returns the code of the videogame.
        
        Returns:
            An integer with the code of the videogame.
        """
        return self.__code

    def set_description(self, description: str):
        """This method changes the description of the videogame.
        
        Args:
            description (str): New description of the videogame.
        """
        self.__description = description

    def __str__(self) -> str:
        return f"{'='*10}\nCode: {self.__code}\n\
            Name: {self.__name}\nDescription: {self.__description}"
