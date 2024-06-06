


/* STORE PROCEDURE: UGLY REPORT */
CREATE PROCEDURE report_ugly()
BEGIN
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

/* POSTGRES 
 * 
 * CREATE PROCEDURE report_ugly
 * LANGUAGE SQL
 * BEGIN ATOMIC
 * 		...
 * END
 * */

CALL report_ugly(); 


CREATE TABLE IF NOT EXISTS LOG_COUNTRY (
	id_log INT AUTO_INCREMENT PRIMARY KEY,
	operation VARCHAR(30),
	country_code INT,
	date_log TIMESTAMP DEFAULT NOW()
);

DROP TRIGGER insert_country;
CREATE TRIGGER insert_country
AFTER INSERT ON country
FOR EACH ROW
	INSERT INTO LOG_COUNTRY(operation, country_code)
	VALUES ("NEW COUNTRY", NEW.code);

INSERT INTO country(code, name) VALUES (57,'Colombia');
SELECT * FROM country;
SELECT * FROM LOG_COUNTRY;

CREATE TRIGGER update_country
AFTER UPDATE ON country
FOR EACH ROW
	INSERT INTO LOG_COUNTRY(operation, country_code)
	VALUES ("UPDATE COUNTRY", NEW.code);

UPDATE country SET name='Chibchombia' WHERE code=57;

/* VIEW */ 
CREATE VIEW popular_users_view AS 
	SELECT users.name, users.email, users.nickname, country.name as 'country',
    	   bank_account.bank_name AS bank, bank_account.account_number AS bank_account 
	FROM users 
	JOIN country ON users.country_fk = country.code 
	JOIN bank_account ON bank_account.user_fk = users.id_user 
	ORDER BY users.email 
	LIMIT 3;
SELECT * FROM popular_users_view;

CREATE PROCEDURE colombian_subscribe_channels()
BEGIN
	DROP VIEW view_colombian_subscribe_channels;
	CREATE VIEW view_colombian_subscribe_channels AS
		SELECT channel.name AS 'channel', channel.description, users.name AS 'username' 
		FROM channel
		JOIN subscribers_rel 
     		ON subscribers_rel.channel_fk = channel.id_channel
		JOIN users ON subscribers_rel.user_fk = users.id_user
		JOIN country ON users.country_fk = country.code
		JOIN subscribers_count  AS sc ON sc.channel_fk = channel.id_channel 
		WHERE country.name LIKE '%Colombia%'
      		AND sc.counter >= 1;
END;

 SHOW VARIABLES LIKE 'event_scheduler';
SET GLOBAL event_scheduler = ON;

CREATE EVENT colombian_subscribers_report_2
ON SCHEDULE EVERY 1 DAY STARTS '2024-01-01 00:05:00'
DO CALL colombian_subscribe_channels();


SELECT * FROM country;











































