import puppeteer, { Browser, Page } from 'puppeteer'
import { NODE_ENV_VALUES } from '../constants/env'
import { Database } from './Database'
import { Logger } from '.'

export class ScraperGetPosts {
  private _db: Database | undefined = undefined

  constructor () {
    this.startDB()
  }

  startDB (): void {
    this._db = new Database()
  }

  async run (): Promise<void> {
    const page = await this.launchBrowser()
    await this.login(page)
    const users = await this.getUsers()
    console.log({ users })
  }

  async launchBrowser (): Promise<Page> {
    try {
      const browser: Browser = await puppeteer.launch({
        headless: process.env.ENVIRONMENT === NODE_ENV_VALUES.PRODUCTION,
        args: process.env.ENVIRONMENT === NODE_ENV_VALUES.PRODUCTION
          ? ['--no-sandbox', '--disable-extensions', '--lang=en', '--disable-dev-shm-usage', '--disable-gpu', '--incognito']
          : ['--disable-extensions', '--lang=en']
      })
      return await browser.newPage()
    } catch (err) {
      throw new Error('Error when launching browser')
    }
  }

  async login (page: Page): Promise<void> {
    try {
      await page.goto('https://www.instagram.com/accounts/login/')
      await page.waitForSelector('input[name="username"]')
      await page.type('input[name="username"]', process.env.INSTAGRAM_USERNAME!)
      await page.type('input[name="password"]', process.env.INSTAGRAM_PASSWORD!)
      await page.click('button[type="submit"]')
      await page.waitForNavigation()
    } catch (err) {
      throw new Error('Error when logging in')
    }
  }

  async getUsers (): Promise<string[]> {
    const usersDB: Array<Record<string, string>> = await this._db?.getUsers().then((res) => res.rows)
    if (!Array.isArray(usersDB) || usersDB.length === 0) {
      Logger.warningLog('⚠️ There are no users to get posts, please check the database.')
    }
    const users = usersDB.map((user) => user.username)
    return users
  }
}
