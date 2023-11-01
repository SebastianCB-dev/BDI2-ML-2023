import { Pool } from 'pg'
import { Logger } from './Logger'

export class Database {

  pool: Pool | undefined = undefined

  constructor () {
    this.createConnection()
  }

  createConnection (): void {
    this.pool = new Pool({
      connectionString: process.env.POSTGRES_URL,
    })
    // Validate connection
    // Attempt a test query
    this.pool.connect()
      .then(() => {
        Logger.infoLog('✅ Database connection established')
      })
      .catch((err) => {
        Logger.errorLog('❌ Database connection failed')
        Logger.errorLog(err as string)
        throw new Error('Error when connecting to the database')
      })
  }

  getPool () {
    return this.pool
  }
}
