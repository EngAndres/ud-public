CREATE DATABASE football;

USE football;

CREATE TABLE IF NOT EXISTS team (
    code INT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(15),
    coach VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS stadium (
    id_stadium INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    capacity INT,
    place VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS player (
    id_player INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    position VARCHAR(20) DEFAULT '',
    team_fk INT NOT NULL,
    FOREIGN KEY (team_fk) REFERENCES team(code)
); 

CREATE TABLE IF NOT EXISTS t_match (
    id_match INT AUTO_INCREMENT PRIMARY KEY,
    match_date DATE NOT NULL,
    local_fk INT NOT NULL,
    guest_fk INT NOT NULL,
    score_local INT,
    score_guest INT,
    FOREIGN KEY (local_fk) REFERENCES team(code),
    FOREIGN KEY (guest_fk) REFERENCES team(code)
);

