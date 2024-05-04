"""
This file contains the classes and methods to manage the videogames of the application.

Author: Carlos A. Sierra <cavirguezs@udistrital.edu.co>
"""

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from db_connection import PostgresConnection


class VideoGame(BaseModel):
    """This class represents the behavior of a videogame"""

    name: str
    code: int
    description: str
    price: float
    new_launch: bool

    def __init__(self):
        self.connection = PostgresConnection(
            "ud_ap_user", "P4$$w0rd", "localhost", 5432, "ud_ad_project"
        )

    def add_to_db(self):
        session = self.connection.session()
        videogame_db = VideoGameDB(
            name=self.name,
            code=self.code,
            description=self.description,
            price=self.price,
            new_launch=self.new_launch,
        )

        self.session.add(videogame_db)
        self.session.commit()
        self.session.close()

    class Config:
        orm_mode = True


Base = declarative_base()


class VideoGameDB(Base):
    __tablename__ = "videogames"

    name = Column(String)
    code = Column(Integer, primary_key=True)
    description = Column(String)
    price = Column(Float)
    new_launch = Column(Boolean)
