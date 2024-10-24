"""This module has an abstractition for a VideoGame device
and some concrete definitions for VideoGame Devices

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>

 This file is part of Singleton Pattern example at UD.

SingletonPattern-UD is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

SingletonPattern-UD is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with SingletonPattern-UD. If not, see <https://www.gnu.org/licenses/>. 
"""

class GamePreferences:

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(GamePreferences, cls).__new__(cls)
            cls.__instance.initialize()
        return cls.__instance
    
    
    def initialize(self):
        """This method puts default values for game preferences for any
        new user."""
        self.__sound = True
        self.__difficulty = 'normal'

    def get_sound(self) -> bool:
        """This method returns current value for sound.
        
        Returns:
            A boolean value about sound activation.
        """
        return self.__sound

    def switch_sound(self):
        """This method changes current value for
        sound parameter. It means, turns on if sound is
        turn off, and viceversa."""
        self.__sound = False if self.__sound else True

    def get_difficulty(self) -> str:
        """This method returns current user preference for
        difficulty default.
        
        Returns:
            A string with the difficulty value    
        """
        return self.__difficulty

    def set_difficulty(self, new_difficulty: str):
        """This method changes difficulty validating 
        it is in the valid range of options.
        
        Args:
            new_difficulty (str): New difficulty to be setup
        """
        if (new_difficulty != self.__difficulty) and \
            (new_difficulty in ['easy', 'normal', 'hard']):
            self.__difficulty = new_difficulty

    def info(self):
        print(self.get_sound(), self.get_difficulty())
