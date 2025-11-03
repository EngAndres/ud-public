"""
City service for managing city-related operations.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from typing import List, Dict, Any
from repositories.postgresql_conn import PostgresqlConn
from models import CityCreate


class CityService:
    """Service class for city operations following DDD architecture."""

    def __init__(self):
        self.db = PostgresqlConn()

    def add_city(self, city_data: CityCreate) -> bool:
        """Add a new city and relate it to a country."""
        if not self.db.connect():
            return False
        
        try:
            query = """
            INSERT INTO city (name, district, population, countryCode_fk)
            VALUES (%s, %s, %s, %s)
            """
            params = [city_data.name, city_data.district, city_data.population, city_data.countryCode]
            self.db.insert(query, params)
            return True
        finally:
            self.db.close()

    def get_africa_cities_spanish_french(self) -> List[Dict[str, Any]]:
        """Get all city names from Africa with population 100k-1M and Spanish/French language."""
        if not self.db.connect():
            return []
        
        try:
            query = """
            SELECT DISTINCT city.name AS city_name,
                   city.population,
                   country.name AS country_name,
                   countryLanguage.language
            FROM city
            JOIN country ON country.code = city.countryCode_fk
            JOIN countryLanguage ON country.code = countryLanguage.countryCode_fk
            WHERE city.population BETWEEN 100000 AND 1000000
                AND country.continent = 'Africa'
                AND countryLanguage.language IN ('Spanish', 'French')
            ORDER BY city.name
            """
            result = self.db.extract(query)
            return [
                {
                    "city_name": row[0],
                    "population": row[1],
                    "country_name": row[2],
                    "language": row[3]
                }
                for row in result
            ] if result else []
        finally:
            self.db.close()

    def get_top_populous_cities_by_continent(self) -> List[Dict[str, Any]]:
        """Get top 3 most populous cities for each continent using CTE."""
        if not self.db.connect():
            return []
        
        try:
            query = """
            WITH ranked_cities AS (
                SELECT c.name AS city_name,
                       c.population,
                       co.continent,
                       co.name AS country_name,
                       ROW_NUMBER() OVER (PARTITION BY co.continent ORDER BY c.population DESC) as rank
                FROM city c
                JOIN country co ON c.countryCode_fk = co.code
            )
            SELECT continent, city_name, population, country_name, rank
            FROM ranked_cities
            WHERE rank <= 3
            ORDER BY continent, rank
            """
            result = self.db.extract(query)
            return [
                {
                    "continent": row[0],
                    "city_name": row[1],
                    "population": row[2],
                    "country_name": row[3],
                    "rank": row[4]
                }
                for row in result
            ] if result else []
        finally:
            self.db.close()

    def get_cities_count_by_language(self) -> List[Dict[str, Any]]:
        """Get total number of cities by official language using GROUP BY and CTE."""
        if not self.db.connect():
            return []
        
        try:
            query = """
            WITH official_languages AS (
                SELECT cl.language, c.code as country_code
                FROM countryLanguage cl
                JOIN country c ON cl.countryCode_fk = c.code
                WHERE cl.isOfficial = 'T'
            ),
            language_cities AS (
                SELECT ol.language, 
                       COUNT(ct.id) as total_cities
                FROM official_languages ol
                LEFT JOIN city ct ON ol.country_code = ct.countryCode_fk
                GROUP BY ol.language
            )
            SELECT language, total_cities
            FROM language_cities
            ORDER BY total_cities DESC, language
            """
            result = self.db.extract(query)
            return [
                {
                    "language": row[0],
                    "total_cities": row[1]
                }
                for row in result
            ] if result else []
        finally:
            self.db.close()