"""
Router for data extraction endpoints.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from services import CountryService, CityService

router = APIRouter(prefix="/reports", tags=["Data Extraction"])


@router.get(
    "/africa-cities_spanish-french",
    summary="African cities with Spanish/French as language.",
)
async def get_africa_cities_spanish_french() -> List[Dict[str, Any]]:
    """
    Extract all city names of Africa where the city has between
    100,000 and 1,000,000 people and the language is Spanish or French.
    """
    service = CityService()
    try:
        result = service.get_africa_cities_spanish_french()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving Africa cities: {str(e)}"
        ) from e


@router.get(
    "/america-countries-city-stats", summary="America countries city statistics."
)
async def get_america_countries_city_stats() -> List[Dict[str, Any]]:
    """
    For the continent America, for every country, extract how many cities
    it has and the average population of the cities.
    """
    service = CountryService()
    try:
        result = service.get_america_countries_city_stats()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving America city stats: {str(e)}"
        ) from e


@router.get(
    "/highest-life-expectancy-english",
    summary="Highest life expectancy by continent (English countries)",
)
async def get_highest_life_expectancy_english() -> List[Dict[str, Any]]:
    """
    For each continent, extract the name of the country with the highest
    life expectation, considering only countries with English as
    the official language."""
    service = CountryService()
    try:
        result = service.get_countries_highest_life_expectancy_by_continent()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving highest life expectancy: {str(e)}",
        ) from e


@router.get(
    "/top-populous-cities-by-continent",
    summary="Top 3 most populous cities by continent.",
)
async def get_top_populous_cities_by_continent() -> List[Dict[str, Any]]:
    """
    For each continent, list the top 3 most populous cities using a
    common table expression (CTE).
    """
    service = CityService()
    try:
        result = service.get_top_populous_cities_by_continent()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving top populous cities: {str(e)}"
        ) from e


@router.get("/cities-count-by-language", summary="Cities count by official language.")
async def get_cities_count_by_language() -> List[Dict[str, Any]]:
    """
    For each language, show the total number of cities in countries where that
    language is official, using GROUP BY and a CTE.
    """
    service = CityService()
    try:
        result = service.get_cities_count_by_language()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving cities count by language: {str(e)}",
        ) from e
