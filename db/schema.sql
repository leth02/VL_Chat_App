CREATE TABLE IF NOT EXISTS users (
    username text NOT NULL PRIMARY KEY,
    password text NOT NULL,
    salt text,
    email text
);