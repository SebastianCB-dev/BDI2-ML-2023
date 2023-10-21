import process from 'process'
import { config } from 'dotenv'
import { ScraperGetUsers, Logger } from './classes'
import { validateEnv } from './helpers/validateEnv'

// Config environment variables
config()

const existsEnv = validateEnv()
if (!existsEnv) {
  Logger.errorLog('❌ Environment variables are not properly set')
  process.exit(1)
}

const main = async (): Promise<void> => {
  const scraperGetUsers = new ScraperGetUsers()
  try {
    await scraperGetUsers.run()
  } catch (err) {
    Logger.errorLog(err as string)
    throw new Error('Error when running scraper it was not possible to get users, please check the logs')
  }
}

main()
  .catch((error) => {
    Logger.errorLog(error as string)
  })
