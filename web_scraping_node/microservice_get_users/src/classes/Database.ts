import { Pool } from 'pg'
import { Logger } from './Logger'

export class Database {
  constructor () {
    this.createConnection()
  }

  createConnection (): void {
    const pool = new Pool({
      connectionString: 'asd'
    })
    // Validate connection
    // Attempt a test query
    pool.query('SELECT 1', (error, results) => {
      if (error) {
        // The connection is not successful.
        Logger.errorLog('❌ Error with database connection: ' + error.message)
        throw error
      } else {
        // The connection is successful.
        Logger.infoLog('✅ Database connection successful')
      }
    })
  }
}
