-- db_init.sql

CREATE DATABASE IF NOT EXISTS movie_db;

USE movie_db;

CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    title VARCHAR(255),
    type VARCHAR(50),
    genres VARCHAR(255),
    releaseYear INT,
    imdbId VARCHAR(20),
    imdbAverageRating DECIMAL(2, 1),
    imdbNumVotes INT,
    availableCountries TEXT
);

-- Cargar datos del archivo CSV
LOAD DATA LOCAL INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE movies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(url, title, type, genres, releaseYear, imdbId, imdbAverageRating, imdbNumVotes, availableCountries);
