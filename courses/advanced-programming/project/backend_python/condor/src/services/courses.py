"""This module has a definition of the set of services to be used
related to courses. Here a router from FastAPI is used to define.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co> - Jan 2025
"""

from fastapi import APIRouter

from ..repositories.courses import CoursesRepository    

repository = CoursesRepository()
courses_router = APIRouter()

@courses_router.get('/courses/get_by_name/<name>')
def get_course_by_name(name: str) -> list:
    """This method returns a list of courses that match.
    
    Args:
        name (str): The name of the course to search.

    Returns:
        A list of courses that match the name given.
    """
    name = name.lower()
    return repository.get_course_by_name(name)

@courses_router.get("/courses/get_by_code/<code>")
def get_course_by_code(code: int) -> dict:
    """This method returns a course that match the code given.
    
    Args:
        code (int): The code of the course to search.

    Returns:
        A course that match the code given.
    """
    if code < 0:
        return {'error': 'Invalid code'}
    return repository.get_course_by_code(code)
