DROP TYPE IF EXISTS comment_status;
CREATE TYPE comment_status AS ENUM ('PENDING', 'REVIEWED');

CREATE TABLE "comment" (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	user_comment varchar(255),
	comment_status comment_status NOT NULL DEFAULT 'PENDING'
);

COMMENT ON TABLE "comment" IS 'Table that stores the system users';
COMMENT ON COLUMN "comment".id IS 'Unique identifier of the user';
COMMENT ON COLUMN "comment".username IS 'Username of the user';
COMMENT ON COLUMN "comment".comment_status IS 'Current status of the user';

CREATE INDEX idx_comment_comment ON "comment" (comment);
CREATE INDEX idx_comment_username ON "comment" (username);

COMMENT ON INDEX idx_comment_comment IS 'Index on the "comment" column to improve query performance';
COMMENT ON INDEX idx_comment_username IS 'Index on the "username" column to improve query performance';

ALTER TABLE "comment" ADD registration_date TIMESTAMP DEFAULT NOW();
ALTER TABLE "comment" ADD COLUMN user_id INTEGER;

ALTER TABLE "comment"
ADD CONSTRAINT fk_comment_user
FOREIGN KEY (user_id)
REFERENCES "users" (id)
ON DELETE CASCADE
ON UPDATE CASCADE;

SELECT user_comment FROM "comment";
