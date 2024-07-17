DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id TEXT PRIMARY KEY UNIQUE, -- ID CCCD
  email TEXT UNIQUE,
  username TEXT UNIQUE,
  phone TEXT UNIQUE,
  password TEXT
);

CREATE TABLE post (
  post_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT, -- ID CCCD
  name TEXT,
  dob TEXT,
  sex TEXT,
  nationality TEXT,
  home TEXT,
  address TEXT,
  features TEXT,
  issue_date TEXT,
  FOREIGN KEY (user_id) REFERENCES user(id)
);