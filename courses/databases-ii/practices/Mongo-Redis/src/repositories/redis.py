import os
import json
from typing import Any
from redis import Redis
from dotenv import load_dotenv
from i_db import IDB

load_dotenv()

class RedisDB(IDB):
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
    
    def connect(self):
        if self._client is None:
            self._client =  Redis(
                host = os.getenv("REDIS_HOST", 'localhost'),
                port=int(os.getenv("REDIS_PORT")),
                db=int(os.getenv("REDIS_DB")),
                decode_responses=True
            )

        try:
            self._client.ping()
            print("Redis up.")
        except e:
            print("Redis down.")
        
    def get_client(self) -> Redis:
        if self._client is None:
            self.connect()
        return self._client
    
    def get(self, key: str):
        value = self._client.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value: Any, expiry_seconds: int = 300):
        json_value = json.dumps(value, default=str)
        self._client.setex(key, expiry_seconds, json_value)
