CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    areaname TEXT,
    hidden BOOLEAN
);
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topicname TEXT,
    area_id INTEGER REFERENCES areas
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    privileges INTEGER,
    alias TEXT
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    visible BOOLEAN,
    ref_message TEXT
);
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

