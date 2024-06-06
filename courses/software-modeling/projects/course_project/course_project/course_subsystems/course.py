"""
This module has some classes related to courses as Model and DAO
"""

import os
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

metadata = MetaData()

courses_db = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50)),
    Column("description", String(100)),
    Column("price", Float),
    Column("available", Boolean),
)

load_dotenv()

DATABASE_CONNECTION = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
db_conn = create_engine(DATABASE_CONNECTION)
conn = db_conn.connect()
Session = sessionmaker(bind=db_conn)
session = Session()

metadata.create_all(db_conn)

class CourseDE(BaseModel):
    """This is a model to represent a course."""
    name: str
    description: str
    price: float
    available: bool


class CourseDAO():
    """This is a class to represent a course as DAO."""

    @classmethod
    def get_all_courses(self):
        """This is a method to get all courses from database"""
        query = courses_db.select()
        return session.execute(query).fetchall()

    @classmethod
    def get_course_by_name(self, course_name: str):
        """This is a method to get a course by name from database"""
        query = courses_db.select().where(courses_db.c.name == course_name)
        return db_conn.execute(query).fetchone() 

    @classmethod
    def add_course(self, course: CourseDE):
        """This is a method to add a course to database"""
        print(course)
        query = courses_db.insert().values(
            name=course.name,
            description=course.description,
            price=course.price,
            available=course.available
        )
        session.execute(query)
        session.commit()
    

    @classmethod
    def delete_course(self, course_id: int):
        """This is a method to delete a course from database"""
        query = courses_db.delete().where(courses_db.c.id == course_id)
        db_conn.execute(query)
