-- Logs example
CREATE TABLE IF NOT EXISTS LOG_COUNTRY (
    id_log SERIAL PRIMARY KEY,
    operation VARCHAR(30),
    country_code INT,
    date_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION insert_country()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO LOG_COUNTRY(operation, country_code)
    VALUES ('NEW COUNTRY', NEW.code);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_country
AFTER INSERT ON country
FOR EACH ROW
EXECUTE PROCEDURE insert_country();

CREATE OR REPLACE FUNCTION update_country()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO LOG_COUNTRY(operation, country_code)
    VALUES ('UPDATE COUNTRY', NEW.code);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_country
AFTER UPDATE ON country
FOR EACH ROW
EXECUTE PROCEDURE update_country();

UPDATE country SET name='Chibchombia' WHERE code=57;


-- Store Procedure 
CREATE OR REPLACE FUNCTION three_users()
RETURNS TABLE (
    name VARCHAR,
    email VARCHAR,
    nickname VARCHAR,
    country VARCHAR,
    bank VARCHAR,
    bank_account VARCHAR
) AS $$
BEGIN
    RETURN QUERY SELECT users.name, users.email, users.nickname, country.name,
       bank_account.bank_name, bank_account.account_number
    FROM users 
    JOIN country ON users.country_fk = country.code 
    JOIN bank_account ON bank_account.user_fk = users.id_user 
    ORDER BY users.email 
    LIMIT 3;
END;
$$ LANGUAGE plpgsql;

-- Create View
CREATE OR REPLACE VIEW all_musical_genre AS 
    SELECT mg.name, mg.description, 
       COUNT(video.id_video) AS videos  
    FROM musical_genre AS mg
    JOIN video ON video.genre_fk = mg.id_genre
    GROUP BY mg.id_genre;


-- Create Scheduled 
-- PostgreSQL does not support event scheduling in the same way as MySQL.
-- You would need to use an external tool like cron or pg_cron.

CREATE OR REPLACE FUNCTION report_ugly()
RETURNS VOID AS $$
BEGIN
    DROP VIEW IF EXISTS view_report_ugly;
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
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION popular_videos()
RETURNS VOID AS $$
BEGIN
    DROP VIEW IF EXISTS view_popular_videos;
    CREATE VIEW view_popular_videos AS
        SELECT video.*, users.name, users.email  
        FROM video
        JOIN users ON video.user_fk = users.id_user
        WHERE video.likes > 20;
END;
$$ LANGUAGE plpgsql;


