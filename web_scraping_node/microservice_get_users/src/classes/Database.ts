import { Pool } from 'pg'
import { LoggerService as Logger } from '@src/classes/Logger'
import { User } from '@src/interface/User'

export class Database {
  private readonly _logger: Logger = new Logger()
  private _pool: Pool | undefined = undefined

  constructor () {
    this.createConnection()
  }

  /**
   * Establishes a connection pool to the PostgreSQL database using the connection string
   * provided in the `POSTGRES_URL` environment variable. Logs a success message if the
   * connection is established, or logs an error and throws an exception if the connection fails.
   *
   * @throws {Error} If the connection to the database cannot be established.
   */
  createConnection (): void {
    this._pool = new Pool({
      connectionString: process.env.POSTGRES_URL
    })
    // Validate connection
    this._pool
      .connect()
      .then(() => {
        this._logger.infoLog('✅ Database connection established')
      })
      .catch((err) => {
        this._logger.errorLog('❌ Database connection failed')
        this._logger.errorLog(err as string)
        throw new Error('Error when connecting to the database')
      })
  }

  /**
   * Adds or updates a list of users in the database.
   *
   * For each user in the provided array:
   * - If the user does not exist in the database, inserts the user.
   * - If the user exists and their full name has changed, updates the full name.
   * - Logs actions and errors using the internal logger.
   *
   * @param users - An array of `User` objects to be added or updated in the database.
   * @returns A promise that resolves when all users have been processed.
   * @throws {Error} If the database connection is not established.
   */
  async addUsers (users: User[]): Promise<void> {
    for (let i = 0; i < users.length; i++) {
      const { username, fullName } = users[i]
      const existsUser = await this.existUserInDatabase(username)
      if (this._pool === null || this._pool === undefined) {
        this._logger.errorLog('❌ Database connection not established')
        throw new Error('Database connection not established')
      }
      // If the user exists in the database, it is not added
      // but we need to check if the user updated his full name
      if (!existsUser) {
        try {
          await this._pool.query(
            'INSERT INTO users (username, fullname) VALUES ($1, $2)',
            [username, fullName]
          )
          this._logger.infoLog(`✅ User ${username} added to database`)
        } catch (err) {
          this._logger.errorLog(
            `❌ Error when adding user ${username} to database`
          )
          this._logger.errorLog(err as string)
        }
        continue
      }
      // If the user exists in the database, we need to check if the user updated his full name
      const res = await this._pool.query(
        'SELECT fullname FROM users WHERE username = $1',
        [username]
      )
      const oldFullName = res.rows[0].fullname
      // If the user updated his full name, we need to update the database
      if (oldFullName !== fullName) {
        try {
          await this._pool.query(
            'UPDATE users SET fullname = $1 WHERE username = $2',
            [fullName, username]
          )
          this._logger.infoLog(`✅ User ${username} updated in database`)
        } catch (err) {
          this._logger.errorLog(
            `❌ Error when updating user ${username} in database`
          )
          this._logger.errorLog(err as string)
        }
      }
    }
  }

  /**
   * Checks if a user with the specified username exists in the database.
   *
   * @param username - The username to search for in the users table.
   * @returns A promise that resolves to `true` if the user exists, or `false` otherwise.
   * @throws Will throw an error if the database connection is not established.
   */
  async existUserInDatabase (username: string): Promise<boolean> {
    if (this._pool === null || this._pool === undefined) {
      this._logger.errorLog('❌ Database connection not established')
      throw new Error('Database connection not established')
    }
    const res = await this._pool.query(
      'SELECT username FROM users WHERE username = $1',
      [username]
    )
    return res.rows.length > 0
  }
}
