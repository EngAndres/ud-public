"""This module contains the class PostgresDatabaseConnection
that is responsible for connecting to the database.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>"""

from typing import List
from datetime import datetime
import psycopg2

from dao import ProjectDAO

from connections.database_connection import DatabaseConnection


class PostgresDatabaseConnection(DatabaseConnection):
    """This class is responsible for connecting to the database."""

    def __init__(self):
        self._dbname = "postgres"
        self._duser = "postgres"
        self._dpass = "P4$$w0rd"
        self._dhost = "localhost"
        self._dport = "5432"
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self._dbname,
                user=self._duser,
                password=self._dpass,
                host=self._dhost,
                port=self._dport,
            )
        except psycopg2.DatabaseError as e:
            print(f"Postgres Connection Error. {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def list_schemas(self):
        schemas = None
        try:
            query = """
                SELECT schema_name
                FROM information_schema.schemata;
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            schemas_db = cursor.fetchall()
            cursor.close()
            schemas = schemas_db
        except psycopg2.DatabaseError as e:
            print(f"Postgres Execution Error. {e}")

        return schemas

    def create(self, query: str, values: tuple) -> int:
        id_ = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            item_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            id_ = item_id
        except psycopg2.DatabaseError as e:
            print(f"Postgres Add Data Error. {e}")

        return id_

    def update(self, query: str, values: tuple, item_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
        except psycopg2.DatabaseError as e:
            print(f"Postgres Update Data Error. {e}")

    def delete(self, table: str, item_id: int):
        try:
            query = f"""
                DELETE FROM {table}
                WHERE id = %s;
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (item_id,))
            self.connection.commit()
            cursor.close()
        except psycopg2.DatabaseError as e:
            print(f"Postgres Delete Data Error. {e}")

    def get_one(self, query: str, values: tuple) -> ProjectDAO:
        item = None
        try:
            cursor = self.connection.cursor()
            print(cursor.mogrify(query, values))
            cursor.execute(query, values)
            print(query)
            print(values)
            item = cursor.fetchone()
            cursor.close()
        except psycopg2.DatabaseError as e:
            print(f"Postgres Get Data Error. {e}")

        return item

    def get_many(self, query: str, values: tuple = ()) -> List[ProjectDAO]:
        items = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            col_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            def convert_value(value):
                if isinstance(value, datetime):
                    return value.strftime("%Y-%m-%d %H:%M:%S")
                return value

            items = [
                {col: convert_value(val) for col, val in zip(col_names, row)}
                for row in rows
            ]

            print(items)
            cursor.close()
        except psycopg2.DatabaseError as e:
            print(f"Postgres Get Data Error. {e}")

        return items
