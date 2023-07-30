# Standard libraries
import os
import time
from pathlib import Path

# External libraries
from gensim.models import Word2Vec

# Custom libraries
from services.database_service import DatabaseService
from services.logging_service import LoggingService
from preprocessing import Preprocessing
from Word2Vec import ModelWord2Vec

class Model:
    # Public Properties
    logger = LoggingService().get_logging()
    databaseService = None
    preprocessingService = None

    def __init__(self):
        """Constructor
           This function initializes the class
           Set the model and connect to the database
        """
        self.start_db()
        self.preprocessingService = Preprocessing()
        self.W2V = ModelWord2Vec()
    
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
                    print(comment)
                    self.logger.info(f"Processing comment: id. {comment['id']}: {comment['username']}")
                    # Get the BDI for the user
                    bdi = self.databaseService.get_bdi(comment['username'])
                    #TODO: Identify language of the comment and use the correct model
                    # language = self.languageService.identify_language(comment['user_comment'])
                    
                    # Process Comment
                    if (comment["user_comment"] == None or comment["user_comment"] == ""):
                        # TODO: Update the comment status to "PROCESSED"
                        continue
                    processed_comment = self.preprocessingService.process_comment(comment["user_comment"])
                    if (processed_comment == None or processed_comment == ""):
                        # TODO: Update the comment status to "PROCESSED"
                        continue
                    get_bdi_comment = self.preprocessingService.get_bdi_comment(processed_comment)
                    print("")
                    print("")
                    print("")
                    print(processed_comment)
                    print("")
                    print("")
                    print("")


                    
                time.sleep(20)
            except Exception as e:
                self.logger.critical(f"Error with the Model: {e.__str__()}")
                time.sleep(120)
                continue