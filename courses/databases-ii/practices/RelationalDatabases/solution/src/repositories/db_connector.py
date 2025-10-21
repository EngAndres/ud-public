'''
This file has an interface to handle all the databases sources
based on the same structure to ensure SOLID.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
'''

from abc import ABC, abstractmethod

class DBConnector(ABC):
    """This class is the interface to handle all the db connection for all the
    relational sources."""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):\
        pass
        
    @abstractmethod
    def extract(self, query, params):
        pass

    @abstractmethod
    def insert(self, query):
        pass

    @abstractmethod
    def delete(self, table, id):
        pass
    