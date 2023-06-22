import psycopg2

from .logging_service import LoggingService


class DatabaseService:
    logger = LoggingService().get_logging()

    def __init__(self, url):
        # This function initializes the class
        self.conn = psycopg2.connect(
            url, sslmode='require', connect_timeout=10)
        self.cur = self.conn.cursor()

    def get_posts(self):
        # This function gets all the posts
        try:
            self.cur.execute(
                "SELECT post_url FROM posts WHERE post_status='PENDING' LIMIT 4;")
            posts = self.cur.fetchall()
            posts = [post[0] for post in posts]
            return posts
        except Exception as e:
            self.logger.error(f"Error getting posts: {e.__str__()}")

    def create_comment(self, comment_data):
        username = comment_data['username']
        comment_text = comment_data['text']
        # Validate if comment doesn't exist
        comment = self.cur.execute(
            'SELECT user_comment FROM comments WHERE user_comment = %s', (comment_text,))
        if comment is not None:
            self.logger.info(f"Comment already exists: {comment_text}")
            return
        # This function creates a new user in the database
        try:
            self.cur.execute(
                'INSERT INTO comments (username, user_comment) VALUES (%s, %s)', (username, comment_text))
            self.conn.commit()
            self.logger.info(f"Comment created for {username}")
        except Exception as e:
            self.logger.error(
                f"Error creating comment: {comment_text} {e.__str__()}")
            # Rollback in case there is any error
            self.conn.rollback()

    def set_post_done(self, post):
        # This function sets the user as reviewed
        try:
            self.cur.execute(
                "UPDATE posts SET post_status = 'REVIEWED' WHERE post_url = %s;", (post,))
            self.conn.commit()
            self.logger.info(f"Post {post} set as REVIEWED")
        except Exception as e:
            self.logger.error(
                f"Error setting post as REVIEWED: {post} {e.__str__()}")
            # Rollback in case there is any error
            self.conn.rollback()
