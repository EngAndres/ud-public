from abc import ABC, abstractmethod

class AbstractFactory(ABC):

    @abstractmethod
    def return_product(self, type_product: str):
        pass
    