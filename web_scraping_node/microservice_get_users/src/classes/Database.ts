import { Pool } from 'pg'
import { Logger } from './Logger'
import { User } from '../interface/User'

export class Database {
  private _pool: Pool | undefined = undefined

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
        Logger.infoLog('✅ Database connection established')
      })
      .catch((err) => {
        Logger.errorLog('❌ Database connection failed')
        Logger.errorLog(err as string)
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
          Logger.infoLog(`✅ User ${username} added to database`)
        } catch (err) {
          Logger.errorLog(`❌ Error when adding user ${username} to database`)
          Logger.errorLog(err as string)
        }
      }
    }
  }

  async existUserInDatabase (username: string): Promise<boolean> {
    const res = await this._pool!.query('SELECT username FROM users WHERE username = $1', [username])
    return (res.rows.length > 0)
  }
}
