from products import Chairs, Beds
from abstract_factory import AbstractFactory

class VintageChair(Chairs):

    def __init__(self):
        super("Wood", "12.7", False, 300.2)

class VintageBed(Beds):

    def __init__(self):
        super((3, 2.5, 0.5), 600)

class VintageFactory(AbstractFactory):

    def return_product(self, type_product: str):
        if type_product == "chair":
            return VintageChair()
        elif type_product == "bed":
            return VintageBed()
        else:
            return None