"""This module is a main point for an API REST
using FastAPI.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from fastapi import FastAPI

app = FastAPI(
    title="ComputerNetworks",
    version="1.0.1",
    description="This is an API example using python"
)

@app.get("/healthcheck")
def healthcheck():
    """This is a service to check if the API is running."""
    return {"status": "ok"}

@app.get("/students/{name}")
def get_students(name: str):
    """This is a service to get students by name.
    
    Args:
        name(str): Name to be searched.

    Returns:
        A list with the valid names.
    """
    students = [
        'Pepito Perez',
        'Pepita Perez',
        'Juanito Perigollaz',
        'Juanita Perigollaz'
    ]

    response = []
    for student in students:
        if name in student:
            response.append(student)

    return {"reponse": response}
    