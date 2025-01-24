"""This is the main file of this backend. 
It contains the FastAPI app that will be used to create the API endpoints."""

from fastapi import FastAPI

from services import courses_router

app = FastAPI()
app.route(courses_router)
