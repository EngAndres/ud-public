"""
This module contains the data models for Country and CountryLanguage.
"""

from typing import Optional, Literal
from pydantic import BaseModel

ContinentType = Literal['Africa', 'America', 'Asia', 'Europe', 'Oceania']

class Country(BaseModel):
    """Model for a country"""
    code: str
    name: str
    continent: ContinentType
    region: str
    population: Optional[int] = 0
    lifeExpectancy: Optional[float] = 0.0
    surfaceArea: float
    indepYear: int

class CountryWithLanguage(BaseModel):
    """Model for a country with language information"""
    code: str
    name: str
    continent: ContinentType
    region: str
    population: Optional[int] = 0
    lifeExpectancy: Optional[float] = 0.0
    surfaceArea: float
    indepYear: int
    language: str
    isOfficial: bool
    percentage: float

class CountryLanguage(BaseModel):
    """Model for country language"""
    countryCode: str
    language: str
    isOfficial: bool
    percentage: float
