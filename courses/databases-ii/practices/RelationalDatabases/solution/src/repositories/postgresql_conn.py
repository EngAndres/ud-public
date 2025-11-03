"""
This module contains the PostgresqlConn class for managing PostgreSQL database connections.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

import os  # operative system - files or folders
from dotenv import load_dotenv  # process .env
import psycopg2  # postgres
from .db_connector import DBConnector


class PostgresqlConn(DBConnector):
    """This class represents the behavior of a PostgreSQL connector."""

    def __init__(self):
        load_dotenv()  # load the .env in memory
        # private attributes
        self.__host = os.getenv("DB_HOST")
        self.__port = os.getenv("DB_PORT")
        self.__user = os.getenv("DB_USER")
        self.__pass = os.getenv("DB_PASSWORD")
        self.__db = os.getenv("DB_NAME")

        self.__conn = None

    def connect(self):
        """This method open PSQL connection."""
        try:
            self.__conn = psycopg2.connect(
                database=self.__db,
                user=self.__user,
                password=self.__pass,
                host=self.__host,
                port=self.__port,
            )
            return True
        except psycopg2.Error as e:
            print(f"Error generating PSQL connection. {e}")
            return False

    def close(self):
        """Close PostgreSQL connection."""
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None

    def __check_connection(self):
        """This method checks if the connection is open."""
        if self.__conn is None:
            raise psycopg2.OperationalError(
                "Connection is not established. Call connect() method first."
            )

    def is_connected(self) -> bool:
        """This method checks if the connection is open.

        Returns:
            bool: True if the connection is open, False otherwise.
        """
        return self.__conn is not None

    def extract(self, query: str):
        """This method retrieve information from PSQL.

        Args:
            query (str): The query to be executed to retrieve information,
                        including the specific search parameters.

        Returns:
            A cursor iterable.
        """
        self.__check_connection()
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()

    def insert(self, query, params):
        """This method inserts a value into a table of PSQL.

        Args:
            query(str): Query to be executed
            params(list): Elements to be inserted
        """
        self.__check_connection()
        cursor = self.__conn.cursor()
        try:
            cursor.execute(query, tuple(params))
            self.__conn.commit()
        except psycopg2.Error as e:
            print(f"Error executing insert: {e}")
            self.__conn.rollback()
        finally:
            cursor.close()
