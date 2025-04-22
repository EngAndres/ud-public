"""This module is a interface to define the structure of different
databases connections.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

from abc import ABC, abstractmethod

class DBConnection(ABC):
    """This if an interface to define the structure of different
    databases connections.
    """
    
    @abstractmethod
    def connect(self):
        pass