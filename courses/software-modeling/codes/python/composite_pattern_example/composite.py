from abc import ABC, abstractmethod
from typing import List

# =============== Composite Interface ===============
class Item(ABC):

    def get_weight(self):
        pass

    def get_volume(self):
        pass


# =============== Products (Leaf) ===============
class Product(Item):

    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    def get_weight(self):
        return self.weight

    def get_volume(self):
        return None

# ================== Box (Composite) ==================
class Box(Item):

    def __init__(self, volume: tuple):
        self.volume: tuple = volume
        self.items: List[Item] = []
    
    def get_weight(self):
        if len(self.items) > 1:
            weights = [item.get_weight() for item in self.items]
            return sum(weights)
        else:
            return 0

    def get_volume(self):
        return self.volume

    def add_item(self, item: Item):
        self.items.append(item)
