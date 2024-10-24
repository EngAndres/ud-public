from products import Chairs, Beds
from abstract_factory import AbstractFactory

class ModernChair(Chairs):

    def __init__(self):
        super("Aluminium", "3.5", True, 150.6)

class ModernBed(Beds):

    def __init__(self):
        super((2, 1.5, 0.5), 500)

class ModernFactory(AbstractFactory):

    def return_product(self, type_product: str):
        if type_product == "chair":
            return ModernChair()
        elif type_product == "bed":
            return ModernBed()
        else:
            return None