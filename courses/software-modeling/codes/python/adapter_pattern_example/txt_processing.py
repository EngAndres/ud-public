from file_process_interface import FileProcessingInterface

class ReadTXT:

    def readTXT(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    
class TXTAdapter(FileProcessingInterface):
    
    def get_info(self, file_name):
        data = ReadTXT().readTXT(file_name)
        data = dict(data)
        return data