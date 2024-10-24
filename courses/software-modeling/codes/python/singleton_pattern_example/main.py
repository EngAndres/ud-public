"""This module has a basic implementation of two different devices
where the same game is loaded sharing preferences based on Singleton.

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

from devices import Device, PCDeviceGame, MobileDeviceGame

device_1: Device = MobileDeviceGame()
device_2: Device = PCDeviceGame()

print('Start:')
device_1.get_device_preferences()
device_2.get_device_preferences()

print("\n\nMemory references")
print(device_1.preferences)
print(device_2.pc_preferences)

print("\n\nChange on Device 2 and check on Device 1")
device_2.set_device_preference()
device_1.get_device_preferences()
