-- message-app.sql -- for SQLite 3
-- For reference on datatypes in SQLite, please visit https://www.sqlite.org/draft/datatype3.html

--
-- Structure for table users
--

BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL
);

--
-- Structure for table conversation_request
--
DROP TABLE IF EXISTS conversation_request;
CREATE TABLE conversation_request (
    id INTEGER PRIMARY KEY,
    initiator_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    accepted INTEGER NOT NULL, -- 1 means accepted; 0 means has not been accepted or declined; 2 means has been declined
    request_time INTEGER NOT NULL,
    accepted_time INTEGER,
    FOREIGN KEY (initiator_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
);

--
-- Structure for table conversations
--
DROP TABLE IF EXISTS conversations;
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    participants TEXT NOT NULL,
    last_message_id INTEGER
);

--
-- Structure for table messages
--
DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    seen INTEGER NOT NULL, -- 1 means seen and 0 means has not been seen
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
);

--
-- Populate sample data for development
--

INSERT INTO users (id, username, email, password_hash, password_salt) VALUES (1000, 'username1', 'username1@example.com', 'password_hash_1', 'password_salt_1');
INSERT INTO users (id, username, email, password_hash, password_salt) VALUES (1001, 'username2', 'username2@example.com', 'password_hash_2', 'password_salt_2');
INSERT INTO users (id, username, email, password_hash, password_salt) VALUES (1002, 'username3', 'username3@example.com', 'password_hash_3', 'password_salt_3');


COMMIT TRANSACTION;
