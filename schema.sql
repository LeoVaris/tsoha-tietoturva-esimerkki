drop table if exists users;
drop table if exists messages;
drop table if exists notes;

create table users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT
);

create table notes (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users,
  content TEXT,
  private BOOLEAN
);