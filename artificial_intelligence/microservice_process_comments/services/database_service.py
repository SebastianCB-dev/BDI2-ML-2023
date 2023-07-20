import psycopg2

from .logging_service import LoggingService


class DatabaseService:
    logger = LoggingService().get_logging()
        
    def __init__(self, url):
        # This function initializes the class
        self.conn = psycopg2.connect(
            url, sslmode='require', connect_timeout=10)
        self.cur = self.conn.cursor()

    def get_comments(self):
        # This function returns the comments
        self.cur.execute(
            "SELECT id, username, user_comment FROM comments WHERE comment_status = 'PENDING'")
        comments = self.cur.fetchall()
        comments = [{'id': comment[0], 'username': comment[1],
                     'user_comment': comment[2]} for comment in comments]
        return comments

    def get_bdi(self, username):
        # This function returns the bdi
        self.cur.execute(
            "SELECT * FROM bdi WHERE username = %s", (username,))
        bdi = self.cur.fetchone()
        if bdi is None:
            self.create_bdi(username)
        return bdi

    def create_bdi(self, username):
        # This function creates the bdi for the user
        self.cur.execute("INSERT INTO bdi (username) VALUES (%s)", (username,))
        self.conn.commit()
        self.logger.info(f"BDI created for user: {username}")
