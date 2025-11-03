-- Create Database
CREATE DATABASE world_db;

-- Create an app user
CREATE USER test_user WITH PASSWORD 'P4$$w0rd';
GRANT ALL PRIVILEGES ON DATABASE world_db TO test_user;

-- Create Table Country
CREATE TYPE continent_enum AS ENUM ('Africa', 'America', 'Asia',
'Europe', 'Oceania');

CREATE TABLE IF NOT EXISTS country (
	code CHAR(3) PRIMARY KEY,
	name VARCHAR(52) NOT NULL,
	continent continent_enum,
	region VARCHAR(26) NOT NULL,
	population INT DEFAULT 0,
	lifeExpectancy DECIMAL(3, 1) DEFAULT 0.0,
	surfaceArea DECIMAL (10, 2) NOT NULL,
	indepYear SMALLINT NOT NULL
);

INSERT INTO country(code, name, continent, region, population, lifeExpectancy, surfaceArea, indepYear)
VALUES ('COL', 'Colombia', 'America', 'South America', 50000000, 65.2, 50.2, 1819);

-- create table City
CREATE TABLE IF NOT EXISTS city (
	id SERIAL PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	district VARCHAR(20),
	population INT DEFAULT 0,
	countryCode_fk CHAR(3),
	FOREIGN KEY (countryCode_fk) REFERENCES country(code)
);

INSERT INTO city(name, district, population, countryCode_fk)
VALUES ('Bogota', 'Cundinamarca', 8000000, 'COL');
 
-- create table CountryLanguage
CREATE TABLE IF NOT EXISTS countryLanguage (
	countryCode_fk CHAR(3) REFERENCES country(code),
	language VARCHAR(30) NOT NULL,
	isOfficial CHAR(1) CHECK (isOfficial IN ('T', 'F')),
	percentage DECIMAL(4, 1),
	PRIMARY KEY (countryCode_fk, language)
);

INSERT INTO countryLanguage(countryCode_fk, language, isOfficial, percentage)
VALUES ('COL', 'Spanish', 'T', 0.95);

-- 1
SELECT city.name AS city_name
FROM city
JOIN country 
	ON country.code = city.countryCode_fk
JOIN countryLanguage 
	ON country.Code = countryLanguage.countryCode_fk
WHERE city.population BETWEEN 100000 AND 1000000
	AND country.continent = 'Africa'
	AND countryLanguage.language IN ('Español', 'Frances');
 
	
-- 2
