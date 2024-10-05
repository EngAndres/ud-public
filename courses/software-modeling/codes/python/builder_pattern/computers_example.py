from abc import ABC, abstractmethod

# ========================== Product ===================== #
class Computer:
    
    def __init__(self):
         pass
    
    def set_board(self, board: str):
        self.board = board

    def set_ram(self, ram: int):
        self.ram = ram
    
    def set_processor(self, processor: str):
        self.processor = processor

    def __str__(self):
        return f"Board: {self.board}\nRAM: {self.ram}\nProcessor: {self.processor}"

# ========================== Builder Pattern =============== #
class ComputerBuilder(ABC):
    
    @abstractmethod
    def build_board(self):
        pass

    @abstractmethod
    def build_ram(self):
        pass

    @abstractmethod
    def build_processor(self):
        pass

    @abstractmethod
    def get_product(self):
        pass


class BuilderLaptop(ComputerBuilder):
    
    def build_board(self):
        pass

    def build_ram(self):
        pass

    def build_processor(self):
        pass

    def get_product(self):
        pass



class BuilderGamer(ComputerBuilder):

    def __init__(self):
        self.computer = Computer()

    def build_board(self):
        self.computer.set_board("Board ASUS")

    def build_ram(self):
        self.computer.set_ram(16)

    def build_processor(self):
        self.computer.set_processor("AMD Ryzen GPU")

    def get_product(self) -> Computer:
        return self.computer
    
    
class BuilderHome(ComputerBuilder):
    
    def __init__(self):
        self.computer = Computer()

    def build_board(self):
        self.computer.set_board("Board MSI")

    def build_ram(self):
        self.computer.set_ram(2)

    def build_processor(self):
        self.computer.set_processor("Intel Celeron")

    def get_product(self) -> Computer:
        return self.computer

# ======================== Director =================== #
class Director:

    def __init__(self, builder: ComputerBuilder):
        self.builder = builder

    def make(self):
        self.builder.build_board()
        self.builder.build_ram()
        self.builder.build_processor()
        return self.builder.get_product()


#============ Client ============#
if __name__ == "__main__":
    builder_gamer = BuilderGamer()
    builder_home = BuilderHome()
    builder_laptop = BuilderLaptop()

    type_ = input("Enter computer type:") 
    
    if type_ == "gamer":
        director = Director(builder_gamer)
    elif type_ == "home":
        director = Director(builder_home)
    elif type_ == "laptop":
        director = Director(builder_laptop)
    
    computer = director.make()
    print(computer)