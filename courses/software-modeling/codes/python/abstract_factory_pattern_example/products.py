class Product:

    def __init__(self, max_weight: float):
        self.max_weight = max_weight

    def is_enough(self, person_weight: float) -> bool:
        return True if person_weight < self.max_weight else False

class Chairs(Product):

    def __init__(self, material: str, weight: float, wheels: bool, max_weight: float):
        self.material = material
        self.weight = weight
        self.wheels = wheels
        super(max_weight)

class Beds(Product):

    def __init__(self, dimensions: tuple, max_weight: float):
        self.dimensions = dimensions
        super(max_weight)
    