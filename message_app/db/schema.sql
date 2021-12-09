CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    accepted BOOLEAN NOT NULL DEFAULT 0 CHECK (accepted IN (0,1)),
    requested_time INTEGER NOT NULL,
    accepted_time INTEGER,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS current_messages(
    id_message INTEGER  PRIMARY KEY AUTOINCREMENT,
    messages_content TEXT NOT NULL,
    time_stamps iINTEGERnt NOT NULL,
    seen BOOLEAN NOT NULL DEFAULT 0 CHECK (accepted IN (0,1)),
    sender_id INTEGER NOT NULL,
    reciever_id INTEGER NOT NULL, 
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS all_messages(
    id_message INTEGER  PRIMARY KEY AUTOINCREMENT,
    messages_content TEXT NOT NULL,
    time_stamps iINTEGERnt NOT NULL,
    seen BOOLEAN NOT NULL DEFAULT 0 CHECK (accepted IN (0,1)),
    sender_id INTEGER NOT NULL,
    reciever_id INTEGER NOT NULL, 
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
);