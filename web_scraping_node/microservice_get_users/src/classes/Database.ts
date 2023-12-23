import { Pool } from 'pg'
import { LoggerService as Logger } from './Logger'
import { User } from '../interface/User'

export class Database {
  private _pool: Pool | undefined = undefined
  private _logger: Logger = new Logger()

  constructor () {
    this.createConnection()
  }

  createConnection (): void {
    this._pool = new Pool({
      connectionString: process.env.POSTGRES_URL
    })
    // Validate connection
    this._pool.connect()
      .then(() => {
        this._logger.infoLog('✅ Database connection established')
      })
      .catch((err) => {
        this._logger.errorLog('❌ Database connection failed')
        this._logger.errorLog(err as string)
        throw new Error('Error when connecting to the database')
      })
  }

  async addUsers (users: User[]): Promise<void> {
    for (let i = 0; i < users.length; i++) {
      const { username, fullName } = users[i]
      const existsUser = await this.existUserInDatabase(username)
      if (!existsUser) {
        try {
          await this._pool!.query('INSERT INTO users (username, fullname) VALUES ($1, $2)', [username, fullName])
          this._logger.infoLog(`✅ User ${username} added to database`)
        } catch (err) {
          this._logger.errorLog(`❌ Error when adding user ${username} to database`)
          this._logger.errorLog(err as string)
        }
      }
    }
  }

  async existUserInDatabase (username: string): Promise<boolean> {
    const res = await this._pool!.query('SELECT username FROM users WHERE username = $1', [username])
    return (res.rows.length > 0)
  }
}
