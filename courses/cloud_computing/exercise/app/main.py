"""
This is the entrypoint of my services
based on python.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from fastapi import FastAPI

from src import extract_router, services_router

app = FastAPI(title='UD Cloud Computing Course', version='0.2')

app.include_router(extract_router)
app.include_router(services_router)

@app.get("/")
def root():
    return {"status": "Hola UD!"}


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
