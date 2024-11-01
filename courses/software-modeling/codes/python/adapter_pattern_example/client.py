from json_processing import JSONAdapter
from txt_processing import TXTAdapter
from file_process_interface import FileProcessingInterface

if __name__ == "__main__":
    txt = TXTAdapter()
    json = JSONAdapter()
    
    file_management: FileProcessingInterface = None
    path = "file.txt"

    if path.endswith(".txt"):
        file_management = TXTAdapter()
    elif path.endswith(".json"):
        file_management = JSONAdapter()

    print(file_management.get_info(path))