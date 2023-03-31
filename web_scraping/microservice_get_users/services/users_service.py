import psycopg2


class UsersService:
  def __init__(self, host, port, database, user, password):
    print(host, port, database, user, password)
    self.conn = psycopg2.connect(
      host=host,
      port=port,
      dbname=database,
      user=user,
      password=password
    )
    self.cur = self.conn.cursor()


  def getUsers(self):
    self.cur.execute('SELECT username FROM users')    
    return self.cur.fetchall()
