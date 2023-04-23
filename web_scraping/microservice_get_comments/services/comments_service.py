import psycopg2

from .logging_service import LoggingService

class CommentsService:
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


  def get_comment(self):
    # This function gets all users from the database
    self.cur.execute('SELECT comment FROM comments LIKE %s', '%test%')
    data = self.cur.fetchall()
    return [row[0] for row in data]

  def create_comment(self, comment_data):
    username = comment_data['username']
    comment = comment_data['text']
    print('comment', comment)
    # Validate if comment doesn't exist
    comment = self.cur.execute('SELECT user_comment FROM comment WHERE user_comment = %s', (comment,))
    if comment is not None:
      self.logger.info(f"Comment already exists: {comment}")
      return
    # This function creates a new user in the database
    try:
      self.cur.execute('INSERT INTO comment (username, user_comment) VALUES (%s, %s)', (username, comment))
      self.conn.commit()
      self.logger.info(f"Comment created for {username}")
    except Exception as e:
      self.logger.error(f"Error creating comment: {comment} {e.__str__()}")
      # Rollback in case there is any error
      self.conn.rollback()
