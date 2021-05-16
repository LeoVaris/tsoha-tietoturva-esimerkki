drop table if exists users;
drop table if exists messages;

create table users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT
);

create table messages (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users,
  content TEXT,
  private BOOLEAN
);