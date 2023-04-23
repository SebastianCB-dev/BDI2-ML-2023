
DROP TYPE IF EXISTS comment_status;
CREATE TYPE comment_status AS ENUM ('PENDING', 'REVIEWED');

CREATE TABLE comments (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	comment varchar(255),
	comment_status comment_status NOT NULL DEFAULT 'PENDING'
);

COMMENT ON TABLE "comments" IS 'Table that stores the system users';
COMMENT ON COLUMN "comments".id IS 'Unique identifier of the user';
COMMENT ON COLUMN "comments".username IS 'Username of the user';
COMMENT ON COLUMN "comments".comment_status IS 'Current status of the user';

CREATE INDEX idx_comment_comment ON "comments" (comment);
CREATE INDEX idx_comment_username ON "comments" (username);

COMMENT ON INDEX idx_comment_comment IS 'Index on the "comment" column to improve query performance';
COMMENT ON INDEX idx_comment_username IS 'Index on the "username" column to improve query performance';

ALTER TABLE "comments" ADD registration_date TIMESTAMP DEFAULT NOW();
ALTER TABLE "comments" ADD COLUMN user_id INTEGER;

ALTER TABLE "comments"
ADD CONSTRAINT fk_comment_user
FOREIGN KEY (user_id)
REFERENCES "users" (id)
ON DELETE CASCADE
ON UPDATE CASCADE;

SELECT * FROM "comments";