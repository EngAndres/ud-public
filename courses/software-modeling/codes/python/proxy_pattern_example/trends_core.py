from abc import ABC, abstractmethod
import json

# ================ TrendsInterface ================
class TrendsInterface(ABC):

    @abstractmethod
    def get_trends(self, type_: str):
        """This method lets you get the trends.
        
        Args:
            type_ (str): The type of the trends.

        Returns:
            A dictionary with the trends of an specific type.
        """


# ================ Trends ================
class Trends(TrendsInterface):

    def get_trends(self, type_: str):
        with open("trends.json", "r", encoding="utf-8") as f:
            trends = json.load(f)

        return trends.get(type_)
    