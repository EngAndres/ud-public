"""
This module handles the data for courses in the enrollment process.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co> - Jan 2025
"""
import json

class CourseData:
    """This class represents the data structure of a course."""
    def __init__(self, name, code, enrollments):
        self.name = name
        self.code = code
        self.enrollments = enrollments

class Courses:
    """This class represents the repository of courses."""

    def __init__(self):
        self.course_data = None
        self.file_path = 'repositories/courses.json'
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.course_data = json.load(file)

    def get_course_by_name(self, name: str) -> list:
        """This method returns a list of courses that match 
        the name given as parameter.
        
        Args:
            name (str): The name of the course to search.
        
        Returns:
            A list of courses that match the name given.
        """
        result = []
        for course in self.course_data:
            if name in course['name']:
                course_temp = CourseData(course['name'], course['code'], course['enrollments'])
                result.append(course_temp)
        return result

    def get_course_by_code(self, code: int) -> CourseData:
        """This method returns a course that match the code given as parameter.

        Args:
            code (int): The code of the course to search.

        Returns:
            A course that match the code given.
        """
        result = None
        for course in self.course_data:
            if code == course['code']:
                result = CourseData(course['name'], course['code'], course['enrollments'])
                break
        return result

    def increase_enrollment(self, code: int) -> None:
        """This method increases the enrollment of a course by one.

        Args:
            code (int): The code of the course to increase the enrollment.
        """
        for course in self.course_data:
            if code == course['code']:
                course['enrollments'] += 1
                break

    def decrease_enrollment(self, code: int) -> None:
        """This method decreases the enrollment of a course by one.

        Args:
            code (int): The code of the course to decrease the enrollment.
        """
        for course in self.course_data:
            if code == course['code'] and course['enrollments'] > 0:
                course['enrollments'] -= 1

    def save(self):
        """This method saves the data of the courses in a file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.course_data, f)
