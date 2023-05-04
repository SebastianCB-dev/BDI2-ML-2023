-- This is the script to create the database and the table to store the users
-- You have to run this script in the database to create the table
-- Make sure you have the database created before running this script
DROP TYPE IF EXISTS user_status;

CREATE TYPE user_status AS ENUM ('PENDING', 'REVIEWED');

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL UNIQUE,
	fullname varchar(255),
	user_status user_status NOT NULL DEFAULT 'PENDING'
);

COMMENT ON TABLE users IS 'Table that stores the system users';

COMMENT ON COLUMN users.id IS 'Unique identifier of the user';

COMMENT ON COLUMN users.username IS 'Username of the user';

COMMENT ON COLUMN users.user_status IS 'Current status of the user';

CREATE INDEX idx_users_username ON users (username);

ALTER TABLE
	users
ADD
	registration_date TIMESTAMP DEFAULT NOW();

SELECT
	*
FROM
	users;