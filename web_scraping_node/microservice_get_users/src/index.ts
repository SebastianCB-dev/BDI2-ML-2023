import process from 'process'
import { config } from 'dotenv'
import { ScraperGetUsers, LoggerService as Logger } from '@src/classes'
import { validateEnv } from '@src/helpers/validateEnv'

const logger: Logger = new Logger()

// Config environment variables
config()
const existsEnv = validateEnv()
if (!existsEnv) {
  logger.errorLog('❌ Environment variables are not properly set')
  process.exit(1)
}

const main = async (): Promise<void> => {
  const scraperGetUsers = new ScraperGetUsers()
  while (true) {
    try {
      await scraperGetUsers.run()
      logger.infoLog('✅ Scraper finished')
      logger.infoLog('⏳ Waiting 3 minutes to run again')
      await new Promise((resolve) => setTimeout(resolve, 180000))
      logger.infoLog('⏳ Running scraper again')
    } catch (err) {
      logger.errorLog(err as string)
      throw new Error('Error when running scraper it was not possible to get users, please check the logs')
    }
  }
}

main()
  .catch((error) => {
    logger.errorLog(error as string)
  })
