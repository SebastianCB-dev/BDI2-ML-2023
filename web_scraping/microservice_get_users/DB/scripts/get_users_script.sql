DROP DATABASE BDI_II_ML;
CREATE DATABASE BDI_II_ML WITH ENCODING='UTF8';

DROP TYPE IF EXISTS user_status;
CREATE TYPE user_status AS ENUM ('PENDING', 'REVIEWED');

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL UNIQUE,	
	fullname varchar(255) NOT NULL,
	user_status user_status NOT NULL DEFAULT 'PENDING'
);

COMMENT ON TABLE users IS 'Table that stores the system users';
COMMENT ON COLUMN users.id IS 'Unique identifier of the user';
COMMENT ON COLUMN users.username IS 'Username of the user';
COMMENT ON COLUMN users.user_status IS 'Current status of the user';
CREATE INDEX idx_users_username ON users (username);

ALTER TABLE users ADD registration_date TIMESTAMP DEFAULT NOW();