from trends_core import TrendsInterface, Trends
from datetime import datetime

class ProxyTrends(TrendsInterface):

    def __init__(self):
        self.cache = {}
        self.trends = Trends() # composition

    def __save_log(self, value):
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {value}\n")

    def get_trends(self, type_: str):
        if type_ is self.cache:
            self.__save_log(f"Return trends {type_} from cache")
            return self.cache[type_]
        else:
            data = self.trends.get_trends(type_)
            self.cache[type_] = data
            self.__save_log(f"Return trends {type_} from JSON document")
            return data