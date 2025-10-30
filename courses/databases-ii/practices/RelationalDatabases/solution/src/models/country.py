from pydantic import BaseModel

class Country(BaseModel):
    """Model for a countryS"""
    code: str
    name: str
    continent: str
    region: str
    population: int = None
    lifeExpectancy: float = None
    surfaceArea: float
    indepYear: int
    language: str
    isOfficial: bool
    percentage: float
