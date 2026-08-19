"""
This module demonstrates the use of an index table to speed up searching
in a list of students. It reads student data from a JSON file, creates an
index on the student code, and uses binary search on the index to find
students.
"""

import json
from typing import List, Dict, Any, Tuple

# Global lists to store student data and the index.
students: List[Dict[str, Any]] = []
index: List[Tuple[int, int]] = []


def create_students(filename: str = 'students.json'):
    """Loads student data from a JSON file.

    Args:
        filename: The name of the JSON file to load students from.
                  Defaults to 'students.json'.
    """
    global students
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            students = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        students = []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filename}.")
        students = []


def print_students():
    """Prints the details of all loaded students."""
    if not students:
        print("No students to display.")
        return
    for student in students:
        print(
            f"Nombre: {student.get('nombre', 'N/A')} --- "
            f"Codigo: {student.get('codigo', 'N/A')} --- "
            f"Carrera: {student.get('carrera', 'N/A')}"
        )


def create_index():
    """Creates a sorted index of students based on their code.

    The index is a list of tuples, where each tuple contains a student's
    code and their original index in the `students` list.
    """
    global index
    if not students:
        print("Cannot create index because no students are loaded.")
        return
    # Create a list of (code, original_index) tuples.
    index = [(student['codigo'], i) for i, student in enumerate(students)]
    # Sort the index based on the student code.
    index.sort(key=lambda x: x[0])
    print("Index created and sorted by student code:")
    print(index)


def binary_search_index(code: int) -> int:
    """Performs a binary search on the index to find a student's code.

    Args:
        code: The student code to search for.

    Returns:
        The original index of the student in the `students` list if found,
        otherwise -1.
    """
    lower, upper = 0, len(index) - 1
    while lower <= upper:
        middle = (lower + upper) // 2
        if index[middle][0] == code:
            # Return the original index of the student.
            return index[middle][1]
        if index[middle][0] < code:
            lower = middle + 1
        else:
            upper = middle - 1
    return -1


def search(code: int):
    """Searches for a student by their code using the index.

    Args:
        code: The student code to search for.
    """
    student_i = binary_search_index(code)
    if student_i != -1:
        print(f"\nStudent found: {students[student_i]}")
    else:
        print(f"\nStudent with code {code} not found.")


if __name__ == "__main__":
    # Main execution block.
    create_students()
    if students:
        print("--- All Students ---")
        print_students()
        print("\n--- Index Creation ---")
        create_index()
        print("\n--- Searching for Students ---")
        search(1701)
        search(2023) # Example of a student that might not exist.
