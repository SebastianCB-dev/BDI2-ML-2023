import psycopg2

from .logging_service import LoggingService


class DatabaseService:
    logger = LoggingService().get_logging()

    def __init__(self, url):
        # This function initializes the class
        self.conn = psycopg2.connect(
            url, sslmode='require', connect_timeout=10)
        self.cur = self.conn.cursor()

    def create_post(self, post_url, username):
        # This function creates a post
        try:
            self.cur.execute(
                "INSERT INTO posts (post_url, username) VALUES (%s, %s);", (post_url, username,))
            self.conn.commit()
            self.logger.info(f"Post {post_url} created")
        except Exception as e:
            self.logger.error(
                f"Error creating post: {post_url} {e.__str__()}")

    def get_users(self):
        # This function gets all users from the database
        self.cur.execute(
            "SELECT username FROM users WHERE user_status = 'PENDING' LIMIT 4;")
        data = self.cur.fetchall()
        return [row[0] for row in data]

    def set_done_user(self, username):
        # This function sets the user as reviewed
        try:
            self.cur.execute(
                "UPDATE users SET user_status = 'REVIEWED' WHERE username = %s;", (username,))
            self.conn.commit()
            self.logger.info(f"User {username} set as REVIEWED")
        except Exception as e:
            self.logger.error(
                f"Error setting user as REVIEWED: {username} {e.__str__()}")
            # Rollback in case there is any error
            self.conn.rollback()
