import os
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    _instance = None
    _client = None
    _database = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self):
        if self._client is None:
            # get environmental variables data
            mongo_url = os.getenv("MONGO_DB", "Failed.")
            db_name = os.getenv("MONGO_DB_NAME")

            # set client
            self._client = MongoClient(mongo_url)
            self._database = self._client[db_name]

            # test
            try:
                self._client.admin.command('ping')
                print("Connection stablished.")
            except e:
                print("Connection to Mongo Failed.")

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._database =None

    def get_database(self) -> Database:
        if self._database is None:
            self.connect()
        return self._database
