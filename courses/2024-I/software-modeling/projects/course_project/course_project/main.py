"""
This module is the main entry point where web services are defined
to interact with all external users, including frontend clients
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv
from sqlalchemy import create_engine

from course_subsystems import CourseDE, CourseDAO

# db://user:password@url:port/name_db

app = FastAPI(
    title="Entertaining Backend Project",
    version="0.1",
    description="This is an api web to consume services for a entertaining center.",
)


@app.get("/healtcheck")
def healtcheck():
    """This is a service to validate web services are up."""
    return {
        "Message": "This is a healthcheck of entertaiment center project",
        "version": 1.0,
    }


class Login(BaseModel):
    username: str
    password: SecretStr


@app.post("/login")
def login(user_info: Login) -> bool:
    """This service lets authenticate an user using username and password."""
    # TODO make authentication
    return False


# Services for Manager
@app.get("/manager/watch_scheduling")
def watch_scheduling():
    """This service allows to a manager see full scheduling in the center."""
    return None


@app.get("/manager/report_payments")
def report_payments():
    """This is a service to generate data for a payments report."""
    return None


# Services for Client
@app.get("/client/course_catalog")
def courses_catalog():
    """This service to get full catalog of courses bring in the center."""
    return None


@app.get("/client/reservations_prices")
def reservations_prices():
    """This service is used to provide prices of course to clients"""
    return None


@app.post("/client/reserve_sport_space")
def reserve_sport_space():
    """This is a service to reserve an specific and available sport space"""
    return None


@app.post("/client/payment")
def payment():
    """This is a service where the client could registers a payment of center servives."""
    return None

@app.post("/manager/create_course", status_code=201)
def create_course(course: CourseDE):
    """This is a service where the manager can create a new course"""
    CourseDAO.add_course(course)
    return {"message": "Course created successfully"}

@app.get("/manager/get_all_courses")
def get_all_courses():
    """This is a service where the manager can get all courses"""
    return CourseDAO.get_all_courses()