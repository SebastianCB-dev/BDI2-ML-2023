DROP TYPE IF EXISTS comment_status;
CREATE TYPE comment_status AS ENUM ('PENDING', 'REVIEWED');

CREATE TABLE "comments" (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	user_comment TEXT,
	comment_status comment_status NOT NULL DEFAULT 'PENDING'
);

COMMENT ON TABLE "comments" IS 'Table that stores the system users';
COMMENT ON COLUMN "comments".id IS 'Unique identifier of the user';
COMMENT ON COLUMN "comments".username IS 'Username of the user';
COMMENT ON COLUMN "comments".comment_status IS 'Current status of the user';

CREATE INDEX idx_comments_comment ON "comments" (user_comment);
CREATE INDEX idx_comments_username ON "comments" (username);

COMMENT ON INDEX idx_comments_comment IS 'Index on the "comment" column to improve query performance';
COMMENT ON INDEX idx_comments_username IS 'Index on the "username" column to improve query performance';

ALTER TABLE "comments" ADD registration_date TIMESTAMP DEFAULT NOW();

SELECT user_comment FROM "comments";
