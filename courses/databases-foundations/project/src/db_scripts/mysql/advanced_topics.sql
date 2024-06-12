-- Logs example
CREATE TABLE IF NOT EXISTS LOG_COUNTRY (
	id_log INT AUTO_INCREMENT PRIMARY KEY,
	operation VARCHAR(30),
	country_code INT,
	date_log TIMESTAMP DEFAULT NOW()
);

CREATE TRIGGER insert_country
AFTER INSERT ON country
FOR EACH ROW
	INSERT INTO LOG_COUNTRY(operation, country_code)
	VALUES ("NEW COUNTRY", NEW.code);

CREATE TRIGGER update_country
AFTER UPDATE ON country
FOR EACH ROW
	INSERT INTO LOG_COUNTRY(operation, country_code)
	VALUES ("UPDATE COUNTRY", NEW.code);

UPDATE country SET name='Chibchombia' WHERE code=57;


-- Store Procedure 
CREATE PROCEDURE three_users()
BEGIN
	SELECT users.name, users.email, users.nickname, country.name as 'country',
       bank_account.bank_name AS bank, bank_account.account_number AS bank_account 
	FROM users 
	JOIN country ON users.country_fk = country.code 
	JOIN bank_account ON bank_account.user_fk = users.id_user 
	ORDER BY users.email 
	LIMIT 3;
END;

-- Create View
CREATE VIEW all_musical_genre AS 
	SELECT mg.name, mg.description, 
       COUNT(video.id_video) AS videos  
	FROM musical_genre AS mg
	JOIN video ON video.genre_fk = mg.id_genre
	GROUP BY mg.id_genre;


-- Create Scheduled 
SET GLOBAL event_scheduler = ON;

CREATE PROCEDURE report_ugly()
BEGIN
	DROP VIEW view_report_ugly;
	CREATE VIEW view_report_ugly AS
		SELECT v.name, v.date_upload as video_date, 
		v.likes as video_likes, v.dislikes as video_dislikes,
		c.content AS comment_content, c.likes as comment_likes, 
		c.dislikes as comment_dislikes, c.date_creation as comment_date,
		u.name as comment_user, u.email as user_email
		FROM comment as c
		JOIN users as u ON c.user_fk = u.id_user 
		JOIN video as v ON c.video_fk = v.id_video 
		WHERE c.content LIKE '%ugly%';
END;
CREATE EVENT report_ugly_event
ON SCHEDULE EVERY 1 DAY STARTS '2024-01-01 00:00:00'
DO CALL report_ugly();




CREATE PROCEDURE popular_videos()
BEGIN
	DROP VIEW view_popular_videos;
	CREATE VIEW view_popular_videos AS
		SELECT video.*, users.name, users.email  
		FROM video
		JOIN users ON video.user_fk = users.id_user
		WHERE video.likes > 20;
END;
CREATE EVENT popular_videos
ON SCHEDULE EVERY 3 HOUR STARTS '2024-01-01 00:00:00'
DO CALL popular_videos();



