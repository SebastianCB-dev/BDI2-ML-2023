# Standard libraries
import os

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
        #self.set_model()
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