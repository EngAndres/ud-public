// 1
SELECT city.Name AS city_name
FROM city
JOIN country 
	ON country.Code = city.CountryCode
JOIN countryLanguage 
	ON country.Code = countryLanguage.CountryCode
WHERE city.Population BETWEEN 100000 AND 1000000
	AND country.Continent = 'Africa'
	AND countryLanguage.'Language' IN ('Español', 'Frances');
 
	
// 2
