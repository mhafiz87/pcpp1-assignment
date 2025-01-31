-- SQLite
-- DROP TABLE riders;

CREATE TABLE IF NOT EXISTS riders (
    rider_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rider_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    age INTEGER DEFAULT 18,
    email TEXT NOT NULL
);

INSERT INTO riders VALUES (1, 'Ali','012-345 6789', 35, 'aliali123@gmail.com');
INSERT INTO riders VALUES (2, 'Abu','011-123 4567', 27, '12abu12@gmail.com');
INSERT INTO riders VALUES (3, 'Ahmad','019-222 3333', 24, '567ahmad@gmail.com');
INSERT INTO riders VALUES (4, 'Aishah','018-333 4444', 20, 'aishah123@gmail.com');
INSERT INTO riders VALUES (5, 'Aiman','017-444 5555', 19, 'aiman666@gmail.com');
INSERT INTO riders VALUES (6, 'Anwar','016-555 6666', 70, 'anwar789@gmail.com');

-- ALTER TABLE riders ADD COLUMN phone_number TEXT;
-- UPDATE riders SET phone_number = '012-345 6789' WHERE rider_id = 1;
-- UPDATE riders SET phone_number = '011-123 4567' WHERE rider_id = 2;
-- UPDATE riders SET phone_number = '019-222 3333' WHERE rider_id = 3;
-- UPDATE riders SET phone_number = '018-333 4444' WHERE rider_id = 4;
-- UPDATE riders SET phone_number = '017-444 5555' WHERE rider_id = 5;
-- UPDATE riders SET phone_number = '016-555 6666' WHERE rider_id = 6;

-- ALTER TABLE riders ADD COLUMN age INTEGER DEFAULT 18;
-- UPDATE riders SET age = 35 WHERE rider_id = 1;
-- UPDATE riders SET age = 27 WHERE rider_id = 2;
-- UPDATE riders SET age = 24 WHERE rider_id = 3;
-- UPDATE riders SET age = 20 WHERE rider_id = 4;
-- UPDATE riders SET age = 19 WHERE rider_id = 5;
-- UPDATE riders SET age = 70 WHERE rider_id = 6;

-- ALTER TABLE riders ADD COLUMN email TEXT;
-- UPDATE riders SET email = 'aliali123@gmail.com' WHERE rider_id = 1;
-- UPDATE riders SET email = '12abu12@gmail.com' WHERE rider_id = 2;
-- UPDATE riders SET email = '567ahmad@gmail.com' WHERE rider_id = 3;
-- UPDATE riders SET email = 'aishah123@gmail.com' WHERE rider_id = 4;
-- UPDATE riders SET email = 'aiman666@gmail.com' WHERE rider_id = 5;
-- UPDATE riders SET email = 'anwar789@gmail.com' WHERE rider_id = 6;