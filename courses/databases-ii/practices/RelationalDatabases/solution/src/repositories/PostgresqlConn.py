'''
This module contains the PostgresqlConn class for managing PostgreSQL database connections.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
'''

import os # operative system - files or folders
from dotenv import load_dotenv # process .env
import psycopg2 # postgres
from .db_connector import DBConnector

class PostgresqlConn(DBConnector):
    """This class represents the behavior of a PostgreSQL connector."""

    def __init__(self):
        load_dotenv() # load the .env in memory
        # private attributes
        self.__host = os.getenv('DB_HOST')
        self.__port = os.getenv('DB_PORT')
        self.__user = os.getenv('DB_USER')
        self.__pass = os.getenv('DB_PASSWORD')
        self.__db = os.getenv('DB_NAME')

        self.conn = None

    def connect(self):
        """This method open PSQL connection."""
        try:
            self.conn = psycopg2.connect(
                database = self.__db,
                user = self.__user,
                password = self.__pass,
                host = self.__host,
                port = self.__port
            )
        except psycopg2.Error as e:
            print(f'Error generating PSQL connection. {e}')

    def close(self):
        """Close PostgreSQL connection."""
        self.conn.close()

    def extract(self, query: str):
        """This method retrieve information from PSQL.
        
        Args:
            query (str): The query to be executed to retrieve information,
                        including the specific search parameters.

        Returns:
            A cursor iterable.
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def insert(self, query, params):
        """This method inserts a value into a table of PSQL.
        
        Args:
            query(str): Query to be executed
            params(list): Elements to be inserted
        """
        cursor = self.conn.cursor()
        cursor.execute(query, tuple(params))
        self.conn.commit()
