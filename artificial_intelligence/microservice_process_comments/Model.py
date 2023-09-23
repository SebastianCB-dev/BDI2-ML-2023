# Standard libraries
from pathlib import Path
import os
import time

# Custom libraries
from preprocessing import Preprocessing
from services.database_service import DatabaseService
from services.logging_service import LoggingService
from Word2Vec import ModelWord2Vec


class CommentsProcessor:
    # Public Properties
    logger = LoggingService().get_logging()
    databaseService = None
    preprocessingService = None
    w2v = None

    def __init__(self):
        """Constructor
           This function initializes the class
           Set the model and connect to the database
        """
        self.start_db()
        self.preprocessingService = Preprocessing()
        self.w2v = ModelWord2Vec()

    def get_logger(self):
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
                    self.logger.info(
                        f"Processing comment: id. {comment['id']}: {comment['username']}")
                    # Get the BDI for the user
                    bdi = self.databaseService.get_bdi(comment['username'])
                    # TODO: Identify language of the comment and use the correct model
                    # language = self.languageService.identify_language(comment['user_comment'])

                    # Process Comment
                    if (comment["user_comment"] == None or comment["user_comment"] == ""):
                        # TODO: Update the comment status to "PROCESSED"
                        continue
                    processed_comment = self.preprocessingService.process_comment(
                        comment["user_comment"])
                    if (processed_comment == None or processed_comment == ""):
                        # TODO: Update the comment status to "PROCESSED"
                        continue
                    #Obtener la similitud de coseno entre el comentario y 
                    #Cada una de las respuestas del inventario de depresión de BECK (BDI-II)
                    cosine_similarity_beck = self.w2v.get_cosine_similarity_BECK(processed_comment)
                    print("cosine_similarity_beck:", cosine_similarity_beck)
                    # Obtener la respuesta por item basandose en la similitud de coseno
                    results_beck = self.w2v.get_result_beck(cosine_similarity_beck)
                    print("El comentario lleno el inventario BECK de esta manera:", results_beck)
                    
                    predict = self.w2v.get_predict(results_beck)
                    print('Predicción:', predict)

                time.sleep(20)
            except Exception as e:
                self.logger.critical(f"Error with the Model: {e.__str__()}")
                time.sleep(120)
                continue
