import psycopg2

from .logging_service import LoggingService

class UsersService:
    logger = LoggingService().get_logging()

    def __init__(self, url):
        # This function initializes the class
        self.conn = psycopg2.connect(
            url, sslmode="require", connect_timeout=10)
        self.cur = self.conn.cursor()

    def get_users(self):
        # This function gets all users from the database
        self.cur.execute("SELECT username FROM users")
        data = self.cur.fetchall()
        return [row[0] for row in data]

    def create_user(self, username, fullname=None):
        # This function creates a new user in the database
        try:
            self.cur.execute(
                "INSERT INTO users (username, fullname) VALUES (%s, %s)", (username, fullname))
            self.conn.commit()
            self.logger.info(f"User created: {username}")
        except Exception as e:
            self.logger.error(f"Error creating user: {username} {e.__str__()}")
            # Rollback in case there is any error
            self.conn.rollback()
