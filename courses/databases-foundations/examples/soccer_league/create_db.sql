-- CREATE DATABASE
CREATE DATABASE soccer;
--USE DATABASE soccer;

-- CREATE TABLES
CREATE TABLE soccer.stadium(
    id_stadium INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    capacity INT,
    place VARCHAR(50)
);

CREATE TABLE soccer.team(
    code INT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(15),
    coach VARCHAR(30) NOT NULL
);

CREATE TABLE soccer.player(
    id_player INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL, 
    age INT,
    position VARCHAR(10) DEFAULT '',
    team_fk INT NOT NULL,
    FOREIGN KEY(team_fk) REFERENCES soccer.team(code)
);

CREATE TABLE soccer.match(
    id_match INT AUTO_INCREMENT PRIMARY KEY,
    stadium_fk INT NOT NULL,
    local_fk INT NOT NULL,
    guest_fk INT NOT NULL,
    score VARCHAR(5),
    FOREIGN KEY(stadium_fk) REFERENCES soccer.stadium(id_stadium),
    FOREIGN KEY(local_fk) REFERENCES soccer.team(code),
    FOREIGN KEY(guest_fk) REFERENCES soccer.team(code)
);

CREATE TABLE soccer.stadium(
    id_stadium INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    capacity INT,
    place VARCHAR(50)
);

CREATE TABLE soccer.team(
    code INT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(15),
    coach VARCHAR(30) NOT NULL
);

-- INSERT DATA
INSERT TABLE soccer.stadium(name, capacity, place) 
VALUES ('Campin', 40000, 'Bogota');

INSERT TABLE soccer.stadium(name, capacity, place)
VALUES ('Metropolitano', 45000, 'Barranquilla');

-- this updates all the stadiums
UPDATE soccer.stadium SET capacity = 0;

-- to update a specific use where
UPDATE soccer.stadium SET capacity = 0 WHERE id_stadium = 1;

-- to delete a row
DELETE FROM soccer.stadium WHERE id_stadium = 1;


ALTER TABLE soccer.stadium ADD COLUMN active BOOLEAN DEFAUTL TRUE;
UPDATE soccer.stadium SET active = FALSE WHERE id_stadium = 1;