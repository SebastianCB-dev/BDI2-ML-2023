import psycopg2

from .logging_service import LoggingService


class DatabaseService:
    logger = LoggingService().get_logging()

    def __init__(self, url):
        # This function initializes the class
        self.conn = psycopg2.connect(
            url, sslmode='require', connect_timeout=10)
        self.cur = self.conn.cursor()
