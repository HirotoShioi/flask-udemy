DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS items;

CREATE TABLE users (id int PRIMARY KEY, username text NOT NULL, password text NOT NULL);
CREATE TABLE items (name TEXT NOT NULL, price REAL NOT NULL);