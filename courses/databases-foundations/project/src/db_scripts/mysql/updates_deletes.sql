-- Manipulate Country table
UPDATE country SET name = 'New Country Name' WHERE code = 1;
DELETE FROM country WHERE code = 1;

-- Maniulate Musical Genre table
UPDATE musical_genre SET name = 'New Genre Name', description = 'New Genre Description' WHERE id_genre = 1;
DELETE FROM musical_genre WHERE id_genre = 1;

-- Manipulate Community table
UPDATE community SET name = 'New Community Name', description = 'New Community Description' WHERE id_community = 1;
DELETE FROM community WHERE id_community = 1;

-- Manipulate Users table
UPDATE users SET name = 'New User Name', email = 'new.email@example.com' WHERE id_user = UUID_TO_BIN('your-uuid-here', 1);
DELETE FROM users WHERE id_user = UUID_TO_BIN('your-uuid-here', 1);

-- Manipulate Community-User Relationship table
UPDATE community_user_rel SET expiration_date = '2023-12-31 23:59:59' WHERE community_fk = 1 AND user_fk = UUID_TO_BIN('your-uuid-here', 1);
DELETE FROM community_user_rel WHERE community_fk = 1 AND user_fk = UUID_TO_BIN('your-uuid-here', 1);

-- Manipulate Playlist table
UPDATE playlist SET name = 'New Playlist Name', likes = 100 WHERE id_playlist = 1 AND user_fk = UUID_TO_BIN('your-uuid-here', 1);
DELETE FROM playlist WHERE id_playlist = 1 AND user_fk = UUID_TO_BIN('your-uuid-here', 1);
