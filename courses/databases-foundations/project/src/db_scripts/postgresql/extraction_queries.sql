/* Extraction Queries */

-- All the videos upload by country, in this case using Colombia as a reference
SELECT video.name, video.description, video.likes, video.dislikes, users.name AS user_name 
FROM video
JOIN users ON video.user_fk = users.id_user 
JOIN country ON users.country_fk  = country.code
WHERE country.name LIKE '%Colombia%';

-- All musical genre and how many videos per genre
SELECT mg.name, mg.description, 
       COUNT(video.id_video) AS videos  
FROM musical_genre AS mg
JOIN video ON video.genre_fk = mg.id_genre
GROUP BY mg.id_genre, mg.name, mg.description;

-- All video info, name and email of user, with more than 20 likes
SELECT video.*, users.name, users.email  
FROM video
JOIN users ON video.user_fk = users.id_user
WHERE video.likes > 20;

-- Channels info, at least one subscriber from a specific country. In this case Colombia is used as reference.
WITH subscribers_count AS (
    SELECT count(*) AS counter, channel_fk 
    FROM subscribers_rel
    GROUP BY channel_fk
)
SELECT channel.name, channel.description, users.name 
FROM channel
JOIN subscribers_rel 
     ON subscribers_rel.channel_fk = channel.id_channel
JOIN users ON subscribers_rel.user_fk = users.id_user
JOIN country ON users.country_fk = country.code
JOIN subscribers_count  AS sc ON sc.channel_fk = channel.id_channel 
WHERE country.name LIKE '%Colombia%'
      AND sc.counter >= 1;

-- Comments info, related with user and video, with comment word "ugly" in the content of the comment
SELECT v.name, v.date_upload as video_date, 
       v.likes as video_likes, v.dislikes as video_dislikes,
       c.content AS comment_content, c.likes as comment_likes, 
       c.dislikes as comment_dislikes, c.date_creation as comment_date,
       u.name as comment_user, u.email as user_email
FROM comment as c
JOIN users as u ON c.user_fk = u.id_user 
JOIN video as v ON c.video_fk = v.id_video 
WHERE c.content LIKE '%ugly%';

-- First three users with country info, bank account and musical genre, sorting by email
SELECT users.name, users.email, users.nickname, country.name as "country",
       bank_account.bank_name AS bank, bank_account.account_number AS bank_account 
FROM users 
JOIN country ON users.country_fk = country.code 
JOIN bank_account ON bank_account.user_fk = users.id_user 
ORDER BY users.email 
LIMIT 3;