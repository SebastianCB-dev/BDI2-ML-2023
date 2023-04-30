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

  def create_post(self, post_url, username):
    # This function creates a post
    try:
      self.cur.execute(
        "INSERT INTO posts (post_url, username) VALUES (%s, %s);", (post_url, username,))
      self.conn.commit()
      self.logger.info(f"Post {post_url} created")
    except Exception as e:
      self.logger.error(
        f"Error creating post: {post_url} {e.__str__()}")
  
  def set_done_user(self, username):
    # This function sets the user as reviewed
    try:
      self.cur.execute(
        "UPDATE users SET user_status = 'REVIEWED' WHERE username = %s;", (username,))
      self.conn.commit()
      self.logger.info(f"User {username} set as REVIEWED")
    except Exception as e:
      self.logger.error(
          f"Error setting user as REVIEWED: {username} {e.__str__()}")
      # Rollback in case there is any error
      self.conn.rollback()
