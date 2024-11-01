from trends_core import TrendsInterface
from proxy import ProxyTrends

class Client:

    def __init__(self, trends_service: TrendsInterface):
        self.trends_service = trends_service

    def get_trends(self):
        type_ = input("Enter the type of trends: ")
        return self.trends_service.get_trends(type_)
    

if __name__ == "__main__":
    client = Client(ProxyTrends()) # Liskov
    print(client.get_trends())