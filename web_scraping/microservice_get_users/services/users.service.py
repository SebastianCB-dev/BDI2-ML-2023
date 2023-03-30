import psycopg2


class UsersService:
  def __init__(self, host, port, database, user, password):
    self.conn = psycopg2.connect(
      host=host,
      port=port,
      database=database,
      user=user,
      password=password
    )
    self.cur = self.conn.cursor()
