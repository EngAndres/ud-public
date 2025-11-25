from abc import ABC, abstractmethod

class IDB(ABC):

    @abstractmethod
    def connect(self):
        pass