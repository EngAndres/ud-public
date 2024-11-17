from abc import ABC, abstractmethod

class FileProcessingInterface(ABC):

    @abstractmethod
    def get_into(self, file_name):
        """This method gets the information of a 
        file based on path provided.
        
        Args:
            file_name (str): The path of the file.

        Returns:
            A string with the infomation of the file.
        """
