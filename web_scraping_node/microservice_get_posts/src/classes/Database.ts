import { Pool } from 'pg'
import { Logger } from './Logger'

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

  async getUsers (): Promise<any> {
    const query = 'SELECT username FROM users where user_status = \'PENDING\' LIMIT 10'
    return await this._pool!.query(query)
  }
}
