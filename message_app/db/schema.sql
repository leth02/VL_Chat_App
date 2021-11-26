DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id int NOT NULL PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL,
    salt text,
    email text
);