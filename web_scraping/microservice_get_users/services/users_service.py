import psycopg2

from .logging_service import LoggingService

class UsersService:
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


  def getUsers(self):
    # This function gets all users from the database
    self.cur.execute('SELECT username FROM users')    
    data = self.cur.fetchall()
    return [row[0] for row in data]

  def createUser(self, username, fullname = None):
    # This function creates a new user in the database
    try:
      self.cur.execute('INSERT INTO users (username, fullname) VALUES (%s, %s)', (username, fullname))
      self.conn.commit()
      self.logger.info(f"User created: {username}")
    except Exception as e:
      self.logger.error(f"Error creating user: {username} {e.__str__()}")
      # Rollback in case there is any error
      self.conn.rollback()
