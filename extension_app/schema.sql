DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS extensions;
DROP TABLE IF EXISTS executed_extensions;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  paid_user TEXT DEFAULT NULL,
  admin TEXT DEFAULT NULL
);

CREATE TABLE extensions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ext_title TEXT NOT NULL,
  ext_description TEXT NOT NULL,
  ext_url TEXT NOT NULL,
  ext_payload TEXT DEFAULT NULL,
  ext_headers TEXT DEFAULT NULL,
  ext_background_colour TEXT DEFAULT NULL,
  ext_image TEXT DEFAULT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE executed_extensions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  extension_id INTEGER NOT NULL,
  extension_status_code TEXT,
  extension_headers TEXT,
  comment TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (extension_id) REFERENCES extensions (id)
);