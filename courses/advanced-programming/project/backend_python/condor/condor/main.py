"""This is the main file of this backend. 
It contains the FastAPI app that will be used to create the API endpoints."""

from fastapi import FastAPI

from services.courses import courses_router

app = FastAPI(
    title='Condor API',
    description='This is the API of the Condor project',
    version='0.5'
)
app.include_router(courses_router)
