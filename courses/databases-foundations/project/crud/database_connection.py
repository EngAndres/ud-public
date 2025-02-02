"""This module contains the class PostgresDatabaseConnection 
that is responsible for connecting to the database.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>"""

import psycopg2

class PostgresDatabaseConnection:
    """This class is responsible for connecting to the database."""

    def __init__(self):
        self._dbname = "condor"
        self._duser = "postgres"
        self._dpass = "P4$$w0rd"
        self._dhost = "localhost"
        self._dport = "5432" 
        self.connection = None

    def connect(self):
        """This method connects to the database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self._dbname,
                user=self._duser,
                password=self._dpass,
                host=self._dhost,
                port=self._dport
            )
        except Exception as e:
            print(e)