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

from abc import ABC, abstractmethod
from preferences_singleton import GamePreferences

class Device(ABC):
    """
    This class is an interface to define any video game device
    into the application.
    """

    @abstractmethod
    def set_device_preference(self, **changes):
        """This method changes the preferences of the videogame."""

    @abstractmethod
    def get_device_preferences(self):
        """This method returns the current preferences of the videogame."""


class MobileDeviceGame(Device):

    def __init__(self):
        self.preferences = GamePreferences()

    def set_device_preference(self, **changes):
        preference = changes.get('preference')
        if preference == 'sound':
            self.preferences.switch_sound()
        elif preference == 'difficulty':
            new_difficulty = changes.get('value')
            self.preferences.set_difficulty(new_difficulty)

    def get_device_preferences(self):
        print(f'Difficulty: {self.preferences.get_difficulty()}\n\
            Sound Active: {"ON" if self.preferences.get_sound() else "OFF"}')

class PCDeviceGame(Device):

    def __init__(self):
        self.pc_preferences = GamePreferences()

    def set_device_preference(self, **changes):
        self.pc_preferences.switch_sound()

    def get_device_preferences(self):
        return self.pc_preferences.info()
