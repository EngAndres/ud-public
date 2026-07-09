import json

students = []
index = []

def create_students():
    global students
    with open('students.json', 'r', encoding='utf-8') as file:
        students = json.load(file)

def print_students():
    for student in students:
        print(f'Nombre: {student['nombre']} --- Codigo: {student['codigo']} --- Carrera: {student['carrera']}')

def create_index():
    global index
    for i, student in enumerate(students):
        index.append((student['codigo'], i))
    index = sorted(index, key=lambda x: x[0])
    print(index)

def binary_search_index(code: int):
    lower = 0
    upper = len(index) -1
    while lower <= upper:
        middle = (lower + upper) // 2
        if index[middle][0] == code:
            return index[middle][1]
        if index[middle][0] < code:
            lower = middle + 1
        else:
            upper = middle - 1
    return -1 

def search(code: int):
    student_i = binary_search_index(code)
    if student_i != -1:
        print(students[student_i])
    else:
        print("Student not found")

create_students()
print_students()
create_index()
search(1701)
