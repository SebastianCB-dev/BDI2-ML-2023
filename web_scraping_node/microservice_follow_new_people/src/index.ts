import process from 'process'
import { config } from 'dotenv'
import { ScraperFollowNewPeople, Logger } from './classes'
import { validateEnv } from './helpers/validateEnv'

// Config environment variables
config()
const existsEnv = validateEnv()
if (!existsEnv) {
  Logger.errorLog('❌ Environment variables are not properly set')
  process.exit(1)
}

const main = async (): Promise<void> => {
  const scraperFollowNewPeople = new ScraperFollowNewPeople()
  while (true) {
    try {
      await scraperFollowNewPeople.run()
      Logger.infoLog('✅ Scraper finished')
      Logger.infoLog('⏳ Waiting 3 minutes to run again')
      await new Promise((resolve) => setTimeout(resolve, 180000))
      Logger.infoLog('⏳ Running scraper again')
    } catch (err) {
      Logger.errorLog(err as string)
      throw new Error('Error when running scraper it was not possible to get users, please check the logs')
    }
  }
}

main()
  .catch((error) => {
    Logger.errorLog(error as string)
  })
