class Student:
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

class Course:
    def __init__(self, name: str):
        self.name = name
        self.students = []

    def add_student(self, student: Student):
        if not student in self.students:
            self.students.append(student)
            print(f'El estudiante {student.name} se ha agregado al curso {self.name}.')
        else:
            print('El estudiante ya existe en el curso.')

    def search_student_by_code(self, code: int):
        index = -1
        for i, student in enumerate(self.students):
            if student.code == code:
                index = i
                break
        return index

# =============================

class EnrollmentSystem:
    def __init__(self):
        self.courses = []

    def create_course(self):
        name = input("Ingrese el nombre del curso:")
        new_course = Course(name)
        self.courses.append(new_course)
        print("Curso creado exitosamente.")

    def add_student(self):
        name = input("Ingrese el nombre del estudiante:")
        try:
            code = input("Ingrese el código del estudiate:")
            code = int(code)
        except Exception as e:
            raise ValueError("El código agregado no es un código válido.")
        
        course_enrollment = input("Ingrese el nombre del curso al cual ingresará el estudiante:")
        success = False
        for i, course in enumerate(self.courses):
            if course.name == course_enrollment:
                new_student = Student(name, code)
                self.courses[i].add_student(new_student)
                success = True
                break

        if not success:
            print("Hubo un error agregando el estudiante al curso.")

    def list_students(self):
        success = False
        course_enrollment = input("Ingrese el nombre del curso para listar estudiantes:")
        for course in self.courses:
            if course.name == course_enrollment:
                success = True
                print(f"Lista de estudiantes del curso {course_enrollment}:")
                for student in course.students:
                    print(f'\tNombre: {student.name} --- Código: {student.code}')
                break
        if not success:
            print("No se encontro el curso ingresado.")



def main():
    enrollment_sys = EnrollmentSystem()

    MENU = "\n=====\nMENU DE OPCIONES\n1. Crear Curso\n2. Agregar estudiante\n\
3. Ver listado de curso\n4. Salir"

    while True:
        print(MENU)
        option = int(input("Escoja una opción del menú: "))
        if option == 1:
            enrollment_sys.create_course()
        elif option == 2:
            enrollment_sys.add_student()
        elif option == 3:
            enrollment_sys.list_students()
        elif option == 4:
            print("Gracias por utilizar el sistema.")
            break
        else:
            print("Por favor, escoja una opción válida.")

if __name__ == "__main__":
    main()        
