from pydantic import BaseModel

class Country(BaseModel):
    """This class represents the expected data structure for a country"""
    code: int
    name: str

class SubscriberByChannel(BaseModel):
    channel: str
    description: str
    username: str
