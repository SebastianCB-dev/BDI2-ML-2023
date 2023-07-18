# Standard libraries
import os
import time

# Custom libraries
from services.database_service import DatabaseService
from services.logging_service import LoggingService


class Model:
    # Public Properties
    logger = LoggingService().get_logging()
    databaseService = None

    def __init__(self):
        """Constructor
            This function initializes the class
            Set the model and connect to the database
        """
        # self.set_model()
        self.start_db()

    def getLogger(self):
        # This function returns the logger
        return self.logger

    def start_db(self):
        """Database
            This function starts the database connection
            * Set variables from .env file
        """
        self.databaseService = DatabaseService(os.getenv('POSTGRES_URL'))
        self.logger.info("Database connection started")

    def process_comments(self):
        while True:
            try:
                comments = self.databaseService.get_comments()
                for comment in comments:
                    self.logger.info(f"Processing comment: {comment['id']}- {comment['username']}")
                    bdi = self.self.databaseService.get_bdi(comment['user_comment'])
                time.sleep(20)
            except Exception as e:
                time.sleep(120)
                continue
