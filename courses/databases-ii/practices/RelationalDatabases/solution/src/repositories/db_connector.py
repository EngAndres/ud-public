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
        """Open DB connection."""

    @abstractmethod
    def close(self):
        """Close DB connection."""

    @abstractmethod
    def extract(self, query):
        """Retrive information from DB."""

    @abstractmethod
    def insert(self, query, params):
        """Insert new data into the DB."""
