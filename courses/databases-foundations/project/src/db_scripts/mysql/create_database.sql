/******* MySQL Version 8.0 *******/
CREATE DATABASE ud_db_project;
USE ud_db_project;

/*************************************** Contry Table ***************************************/
CREATE TABLE IF NOT EXISTS country (
	code INT PRIMARY KEY,
	name VARCHAR(25) UNIQUE NOT NULL
);
CREATE INDEX IF NOT EXISTS country_name ON country(name);

/*************************************** Musical Genre Table ***************************************/
CREATE TABLE IF NOT EXISTS musical_genre(
	id_genre INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(15) UNIQUE NOT NULL,
	description VARCHAR(100)
);
CREATE INDEX IF NOT EXISTS musical_genre_name ON musical_genre(name);

/*************************************** Community Table ***************************************/
CREATE TABLE IF NOT EXISTS community (
	id_community INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(25) UNIQUE NOT NULL,
	description VARCHAR(200)
);
CREATE INDEX IF NOT EXISTS community_name ON community(name);

/*************************************** Users Table ***************************************/
CREATE TABLE IF NOT EXISTS users (
	id_user BINARY(16) DEFAULT (uuid_to_bin(uuid())),
	name VARCHAR(50) NOT NULL, 
	email VARCHAR(30) UNIQUE NOT NULL,
	phone VARCHAR(50), 
	nickname VARCHAR(20) UNIQUE NOT NULL	, 
	password VARCHAR(30) NOT NULL,
	musical_genre_fk int,
	country_fk int,
	FOREIGN KEY (musical_genre_fk) REFERENCES musical_genre(id_genre),
	FOREIGN KEY (country_fk) REFERENCES country(code)
);
ALTER TABLE users ADD PRIMARY KEY(id_user);
CREATE INDEX user_email ON users(email);
CREATE INDEX user_nickname ON users(nickname);

/*************************************** Community-User Relationship Table ***************************************/
CREATE TABLE IF NOT EXISTS community_user_rel (
	community_fk INT, 
	user_fk BINARY(16),
	expiration_date TIMESTAMP,
	PRIMARY KEY(community_fk, user_fk),
	FOREIGN KEY (community_fk) REFERENCES community(id_community),
	FOREIGN KEY (user_fk) REFERENCES users(id_user)
);
DELIMITER //
CREATE TRIGGER set_expiration_date
BEFORE INSERT ON community_user_rel
FOR EACH ROW
BEGIN
   IF NEW.expiration_date IS NULL THEN
      SET NEW.expiration_date = DATE_ADD(NOW(), INTERVAL 1 WEEK);
   END IF;
END;//
DELIMITER ;

/*************************************** Playlist Table ***************************************/
CREATE TABLE IF NOT EXISTS playlist(
	id_playlist INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	likes INT DEFAULT 0,
	user_fk BINARY(16),
	FOREIGN KEY (user_fk) REFERENCES users(id_user)
);

/*************************************** Bank Account Table ***************************************/
CREATE TABLE IF NOT EXISTS bank_account(
	id_account INT AUTO_INCREMENT PRIMARY KEY,
	bank_name VARCHAR(50) NOT NULL,
	account_number VARCHAR(20) UNIQUE NOT NULL,
	country_fk INT,
	user_fk BINARY(16), 
	FOREIGN KEY (country_fk) REFERENCES country(code),
	FOREIGN KEY (user_fk) REFERENCES users(id_user)
);
CREATE INDEX bank_number_account_index ON bank_account(account_number);

/*************************************** Channel Table ***************************************/
CREATE TABLE IF NOT EXISTS channel(
	id_channel INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(30) NOT NULL,
	description VARCHAR(200),
	user_fk BINARY(16),
	FOREIGN KEY (user_fk) REFERENCES users(id_user)
);
CREATE INDEX channel_name ON channel(name);

/*************************************** Subscribers Relationship Table ***************************************/
CREATE TABLE IF NOT EXISTS subscribers_rel(
	user_fk BINARY(16),
	channel_fk INT,
	pay BOOL DEFAULT false,
	pay_cost FLOAT,
	date_subscription TIMESTAMP DEFAULT NOW(),
	PRIMARY KEY (user_fk, channel_fk),
	FOREIGN KEY (user_fk) REFERENCES users(id_user),
	FOREIGN KEY (channel_fk) REFERENCES channel(id_channel)
);

/*************************************** Video Table ***************************************/
CREATE TABLE IF NOT EXISTS video(
	id_video INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	description VARCHAR(200),
	date_upload TIMESTAMP DEFAULT NOW(),
	likes INT DEFAULT 0,
	dislikes INT DEFAULT 0,
	user_fk BINARY(16),
	genre_fk INT,
	channel_fk INT,
	FOREIGN KEY (user_fk) REFERENCES users(id_user),
	FOREIGN KEY (genre_fk) REFERENCES musical_genre(id_genre),
	FOREIGN KEY (channel_fk) REFERENCES channel(id_channel)
);
CREATE INDEX video_name ON video(name);
CREATE INDEX video_likes ON video(likes);
CREATE INDEX video_dislikes ON video(dislikes);

ALTER TABLE video ADD COLUMN popular BOOL DEFAULT false;
DELIMITER //
CREATE TRIGGER update_popularity
AFTER UPDATE ON video
FOR EACH ROW
BEGIN
   IF NEW.likes > 20 THEN
      UPDATE video SET popular = TRUE WHERE id = NEW.id;
   END IF;
END;//
DELIMITER ;

/*************************************** Playlist-Video Relationship Table ***************************************/
CREATE TABLE IF NOT EXISTS playlist_video_rel(
	playlist_fk INT,
	video_fk INT,
	PRIMARY KEY (playlist_fk, video_fk),
	FOREIGN KEY (playlist_fk) REFERENCES playlist(id_playlist),
	FOREIGN KEY (video_fk) REFERENCES video(id_video)
);

/*************************************** Comment Table ***************************************/
CREATE TABLE IF NOT EXISTS comment(
	id_comment INT AUTO_INCREMENT PRIMARY KEY,
	content VARCHAR(300) NOT NULL,
	date_creation TIMESTAMP DEFAULT NOW(),
	likes INT DEFAULT 0,
	dislikes INT DEFAULT 0,
	user_fk BINARY(16),
	video_fk INT,
	FOREIGN KEY (user_fk) REFERENCES users(id_user),
	FOREIGN KEY (video_fk) REFERENCES video(id_video)
);
