"""
Country service for managing country-related operations.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List, Dict, Any
from repositories.postgresql_conn import PostgresqlConn
from models import CountryWithLanguage


class CountryService:
    """Service class for country operations following DDD architecture."""

    def __init__(self):
        self.db = PostgresqlConn()

    def add_country_with_language(self, country_data: CountryWithLanguage) -> bool:
        """Add a new country including its language information."""
        if not self.db.is_connected():
            return False

        try:
            # Insert country
            country_query = """
            INSERT INTO country (code, name, continent, region, population, lifeExpectancy, surfaceArea, indepYear)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            country_params = [
                country_data.code, country_data.name, country_data.continent,
                country_data.region, country_data.population, country_data.lifeExpectancy,
                country_data.surfaceArea, country_data.indepYear
            ]
            self.db.insert(country_query, country_params)

            # Insert country language
            language_query = """
            INSERT INTO countryLanguage (countryCode_fk, language, isOfficial, percentage)
            VALUES (%s, %s, %s, %s);
            """
            language_params = [
                country_data.code, country_data.language,
                'T' if country_data.isOfficial else 'F', country_data.percentage
            ]
            self.db.insert(language_query, language_params)
            return True
        except Exception as e:
            print(f"Error adding country with language: {e}")
            return False
        finally:
            self.db.close()

    def get_countries_highest_life_expectancy_by_continent(self) -> List[Dict[str, Any]]:
        """
        Get country with highest life expectation by continent 
        (only English official language)."""
        if not self.db.is_connected():
            return []

        try:
            query = """
            WITH english_countries AS (
                SELECT c.code, c.name, c.continent, c.lifeExpectancy,
                       ROW_NUMBER() OVER (PARTITION BY c.continent ORDER BY c.lifeExpectancy DESC) as rn
                FROM country c
                JOIN countryLanguage cl ON c.code = cl.countryCode_fk
                WHERE cl.language = 'English' AND cl.isOfficial = 'T'
            )
            SELECT continent, name, lifeExpectancy
            FROM english_countries
            WHERE rn = 1
            ORDER BY continent
            """
            result = self.db.extract(query)
            return [
                {"continent": row[0], "country_name": row[1], "life_expectancy": float(row[2])}
                for row in result
            ] if result else []
        finally:
            self.db.close()

    def get_america_countries_city_stats(self) -> List[Dict[str, Any]]:
        """Get city count and average population for America continent countries."""
        if not self.db.is_connected():
            return []

        try:
            query = """
            SELECT c.name as country_name,
                   COUNT(ct.id) as city_count,
                   COALESCE(AVG(ct.population), 0) as avg_population
            FROM country c
            LEFT JOIN city ct ON c.code = ct.countryCode_fk
            WHERE c.continent = 'America'
            GROUP BY c.code, c.name
            ORDER BY c.name
            """
            result = self.db.extract(query)
            return [
                {
                    "country_name": row[0],
                    "city_count": row[1],
                    "avg_population": float(row[2])
                }
                for row in result
            ] if result else []
        finally:
            self.db.close()
