"""
This file contains the basic example of classes for the 
Software Design I course.

Author: Carlos Andres Sierra
Date: Mar-13th-2024
"""

class Student: # pylint: disable-too-public-methods
    """This class represents the structure and behaviors of any UD student"""    

    # constructor, type hint is a data type recommendations
    def __init__(self, name: str, lastname: str, phone: str, address: str):
        # attributes of the class
        self.name = name
        self.lastname = lastname

        # protected
        self._phone = phone

        ## private
        self.__address = address

    def get_address(self) -> str:
        """
        This method returns the student' address

        Returns:
        - (str): stundent's address
        """
        return self.__address


gclass ComputerStudent(Student):
    """This is a class to represents computer UD students"""

    def __init__(self, name, lastname: str, phone, address):
        super().__init__(name, lastname, phone, address)


student_ = ComputerStudent("Pepe", "Perez", "12345", "St. Evergreen 123")
print(student_.get_address())
print(student_.lastname, student_.name)
