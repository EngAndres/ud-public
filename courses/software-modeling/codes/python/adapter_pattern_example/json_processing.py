import json
from file_process_interface import FileProcessingInterface

class ReadJSON:

    def readJSON(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
class JSONAdapter(FileProcessingInterface):

    def get_info(self, file_name):
        data = ReadJSON().readJSON(file_name)
        if "name" in data:
            data["name"] = data["name"].upper()
        return data