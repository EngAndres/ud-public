/******* PostgreSQL Version 14 *******/

CREATE DATABASE ud_db_project;
\c ud_db_project;

-- Country Table
CREATE TABLE IF NOT EXISTS country (
    code SERIAL PRIMARY KEY,
    name VARCHAR(25) UNIQUE NOT NULL
);
CREATE INDEX IF NOT EXISTS country_name ON country(name);

-- Musical Genre Table
CREATE TABLE IF NOT EXISTS musical_genre(
    id_genre SERIAL PRIMARY KEY, 
    name VARCHAR(15) UNIQUE NOT NULL,
    description VARCHAR(100)
);
CREATE INDEX IF NOT EXISTS musical_genre_name ON musical_genre(name);

-- Community Table
CREATE TABLE IF NOT EXISTS community (
    id_community SERIAL PRIMARY KEY, 
    name VARCHAR(25) UNIQUE NOT NULL,
    description VARCHAR(200)
);
CREATE INDEX IF NOT EXISTS community_name ON community(name);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id_user UUID DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL, 
    email VARCHAR(30) UNIQUE NOT NULL,
    phone VARCHAR(50), 
    nickname VARCHAR(20) UNIQUE NOT NULL, 
    password VARCHAR(30) NOT NULL,
    musical_genre_fk int,
    country_fk int,
    PRIMARY KEY(id_user),
    FOREIGN KEY (musical_genre_fk) REFERENCES musical_genre(id_genre),
    FOREIGN KEY (country_fk) REFERENCES country(code)
);
CREATE INDEX user_email ON users(email);
CREATE INDEX user_nickname ON users(nickname);

-- Community-User Relationship Table
CREATE TABLE IF NOT EXISTS community_user_rel (
    community_fk INT, 
    user_fk UUID,
    expiration_date TIMESTAMP DEFAULT (NOW() + INTERVAL '1 week'),
    PRIMARY KEY(community_fk, user_fk),
    FOREIGN KEY (community_fk) REFERENCES community(id_community),
    FOREIGN KEY (user_fk) REFERENCES users(id_user)
);

-- Playlist Table
CREATE TABLE IF NOT EXISTS playlist(
    id_playlist SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    likes INT DEFAULT 0,
    user_fk UUID,
    FOREIGN KEY (user_fk) REFERENCES users(id_user)
);

-- Bank Account Table
CREATE TABLE IF NOT EXISTS bank_account(
    id_account SERIAL PRIMARY KEY,
    bank_name VARCHAR(50) NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    country_fk INT,
    user_fk UUID, 
    FOREIGN KEY (country_fk) REFERENCES country(code),
    FOREIGN KEY (user_fk) REFERENCES users(id_user)
);
CREATE INDEX bank_number_account_index ON bank_account(account_number);

-- Channel Table
CREATE TABLE IF NOT EXISTS channel(
    id_channel SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(200),
    user_fk UUID,
    FOREIGN KEY (user_fk) REFERENCES users(id_user)
);
CREATE INDEX channel_name ON channel(name);

-- Subscribers Relationship Table
CREATE TABLE IF NOT EXISTS subscribers_rel(
    user_fk UUID,
    channel_fk INT,
    pay BOOL DEFAULT false,
    pay_cost FLOAT,
    date_subscription TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_fk, channel_fk),
    FOREIGN KEY (user_fk) REFERENCES users(id_user),
    FOREIGN KEY (channel_fk) REFERENCES channel(id_channel)
);

-- Video Table
CREATE TABLE IF NOT EXISTS video(
    id_video SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    date_upload TIMESTAMP DEFAULT NOW(),
    likes INT DEFAULT 0,
    dislikes INT DEFAULT 0,
    user_fk UUID,
    genre_fk INT,
    channel_fk INT,
    popular BOOL DEFAULT false,
    FOREIGN KEY (user_fk) REFERENCES users(id_user),
    FOREIGN KEY (genre_fk) REFERENCES musical_genre(id_genre),
    FOREIGN KEY (channel_fk) REFERENCES channel(id_channel)
);
CREATE INDEX video_name ON video(name);
CREATE INDEX video_likes ON video(likes);
CREATE INDEX video_dislikes ON video(dislikes);

-- Trigger to update popularity
CREATE OR REPLACE FUNCTION update_popularity() RETURNS TRIGGER AS $$
BEGIN
   IF NEW.likes > 20 THEN
      NEW.popular := TRUE;
   END IF;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_popularity_trigger
AFTER UPDATE ON video
FOR EACH ROW EXECUTE FUNCTION update_popularity();

-- Playlist-Video Relationship Table
CREATE TABLE IF NOT EXISTS playlist_video_rel(
    playlist_fk INT,
    video_fk INT,
    PRIMARY KEY (playlist_fk, video_fk),
    FOREIGN KEY (playlist_fk) REFERENCES playlist(id_playlist),
    FOREIGN KEY (video_fk) REFERENCES video(id_video)
);

-- Comment Table
CREATE TABLE IF NOT EXISTS comment(
    id_comment SERIAL PRIMARY KEY,
    content VARCHAR(300) NOT NULL,
    date_creation TIMESTAMP DEFAULT NOW(),
    likes INT DEFAULT 0,
    dislikes INT DEFAULT 0,
    user_fk UUID,
    video_fk INT,
    FOREIGN KEY (user_fk) REFERENCES users(id_user),
    FOREIGN KEY (video_fk) REFERENCES video(id_video)
);