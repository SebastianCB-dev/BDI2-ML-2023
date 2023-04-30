DROP TYPE IF EXISTS comment_status;
CREATE TYPE comment_status AS ENUM ('PENDING', 'REVIEWED');

CREATE TABLE "posts" (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	post_url VARCHAR(255),
	post_status post_status NOT NULL DEFAULT 'PENDING'
);

COMMENT ON TABLE "posts" IS 'Table that stores the system users';
COMMENT ON COLUMN "posts".id IS 'Unique identifier of the user';
COMMENT ON COLUMN "posts".username IS 'Username of the user';
COMMENT ON COLUMN "posts".comment_status IS 'Current status of the comment';

CREATE INDEX idx_posts_post_url ON "posts" (post_url);
CREATE INDEX idx_posts_username ON "posts" (username);

COMMENT ON INDEX idx_posts_post_url IS 'Index on the "post_url" column to improve query performance';
COMMENT ON INDEX idx_posts_username IS 'Index on the "username" column to improve query performance';

ALTER TABLE "posts" ADD registration_date TIMESTAMP DEFAULT NOW();

SELECT post_url FROM "comment";
