"""
This module has a class to define a general arcade videogames machine.

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

from videogames import VideoGame

class Machine:
    """This class represents the behavior of an arcade videogames machine."""

    def __init__(self, material: str):
        self.material = material
        self.__videogames = []

    def add_videogame(self, videogame: VideoGame):
        """This method adds a videogame to the current machine.

        In this method a videogame is received as argument,
        following a VideoGame abstract data type, and it is 
        add to internal games list.

        Args:
            videogame (VideoGame): videogame to be added
        """
        self.__videogames.append(videogame)

    def remove_videogame(self, code: int):
        """This method removes a videogame from the machine.

        In this method based on videogame code, if the videogame 
        exists it will be removed from current machine.

        Args:
            code (int): Code of the videogame to be removed.
        """
        index = -1 # logic mark
        for i, vg in enumerate(self.__videogames):
            if vg.get_code() == code:
                index = i
                break

        if index != -1: # videogame is in machine
            self.__videogames.pop(index)
        else:
            print(f"VideoGame with code {code} it not in the machine.")

    def show_videogames(self):
        """This method show all videogames in the current machine.

        In this method the list of videogames is printed following
        a format of code and name.
        """
        if len(self.__videogames) > 0:
            print("Code\tName")
            for vg in self.__videogames:
                print(vg)
        else:
            print("No videogames have been added.")

    def __str__(self) -> str:
        temp_videogames = ""
        for vg in self.__videogames:
            temp_videogames += str(vg)
        return f"{'*'*15}\nMaterial: {self.material}\n\
            Videogames: \n{temp_videogames}"
  