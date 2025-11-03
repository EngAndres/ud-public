"""This module contains the City model."""

from typing import Optional
from pydantic import BaseModel

class City(BaseModel):
    """Model for a city"""
    id: Optional[int] = None
    name: str
    district: Optional[str] = None
    population: int = 0
    countryCode: str

class CityCreate(BaseModel):
    """Model for creating a city"""
    name: str
    district: Optional[str] = None
    population: int = 0
    countryCode: str
