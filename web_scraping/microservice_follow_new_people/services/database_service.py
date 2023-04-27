import psycopg2

from .logging_service import LoggingService

class DatabaseService:
  logger = LoggingService().getLogging()

  def __init__(self, host, port, database, user, password):
    # This function initializes the class
    self.conn = psycopg2.connect(
      host=host,
      port=port,
      dbname=database,
      user=user,
      password=password
    )
    self.cur = self.conn.cursor()
