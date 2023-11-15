import puppeteer, { Browser, ElementHandle, Page } from 'puppeteer'
import { NODE_ENV_VALUES } from '../constants/env'
import { Logger } from './Logger'
import { Database } from './Database'
import { User } from '../interface/User'

export class ScraperGetUsers {
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
    const users: User[] = await this.getUsers(page)
    try {
      await this._db?.addUsers(users)
    } catch (e) {
      throw new Error('Error when adding users to database')
    }
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

  async getUsers (page: Page): Promise<any[]> {
    try {
      if (process.env.INSTAGRAM_USERNAME === undefined) throw new Error('Instagram username is not defined')
      await page.goto(`https://www.instagram.com/${process.env.INSTAGRAM_USERNAME}/following/`)
      const usersContainer = await page.waitForSelector('._aano', { timeout: 5000 })
      if (usersContainer == null) {
        Logger.errorLog('❌ Container with class _aano not found, maybe the class name has changed?')
        throw new Error('')
      }
      await this.scrollToEnd(usersContainer, page)
      const users = await usersContainer.evaluate((element) => {
        const usersSpan = element.querySelectorAll('span._aacl._aaco._aacw._aacx._aad7._aade')
        const fullNamesSpan = element.querySelectorAll('span.x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft')
        const usersStructured: User[] = []
        for (let i = 0; i < usersSpan.length; i++) {
          const user: User = {
            username: usersSpan[i].innerHTML,
            fullName: fullNamesSpan[i].innerHTML
          }
          usersStructured.push(user)
        }
        return usersStructured
      })
      return users
    } catch (err) {
      console.error(err)
      throw new Error('Error Getting the users, maybe the class name has changed? or some script is blocking the page')
    }
  }

  async scrollToEnd (usersContainer: ElementHandle<Element>, page: Page): Promise<void> {
    let previousHeight = 0
    let currentHeight = 0

    do {
      previousHeight = currentHeight
      await usersContainer.evaluate((element) => {
        element.scrollTop = element.scrollHeight
      })
      // Wait for 3 seconds to load the next users
      await new Promise(resolve => setTimeout(resolve, 3000))

      currentHeight = await usersContainer.evaluate((element) => {
        return element.scrollHeight
      })
    } while (previousHeight < currentHeight)
  }
}
