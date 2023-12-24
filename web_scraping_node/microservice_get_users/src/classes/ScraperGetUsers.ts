import puppeteer, { Browser, ElementHandle, Page } from 'puppeteer'
import { NODE_ENV_VALUES } from '../constants/env'
import { LoggerService as Logger } from './Logger'
import { Database } from './Database'
import { User } from '../interface/User'

export class ScraperGetUsers {
  private _db: Database | undefined = undefined
  private _logger: Logger = new Logger()

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
    console.log(users)   
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
        this._logger.errorLog('❌ Container with class _aano not found, maybe the class name has changed?')
        throw new Error('')
      }
      await this.scrollToEnd(usersContainer)
      const users = await usersContainer.evaluate((element) => {
        const usersSpan = element.querySelectorAll('span._ap3a._aaco._aacw._aacx._aad7._aade')
        const fullNamesSpan = element.querySelectorAll('span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')
        const usersStructured: User[] = []
        for (let i = 0; i < usersSpan.length; i++) {
          const user: User = {
            username: usersSpan[i].querySelector('span')?.innerHTML ?? '',
            fullName: fullNamesSpan[i].querySelector('span')?.innerHTML ?? ''
          }
          if (user.username !== '') {
            usersStructured.push(user)
            continue
          }
          this._logger.errorLog(`❌ User ${user.username} not added to the array because it is empty`)
        }
        return usersStructured
      })
      return users
    } catch (err) {
      console.error(err)
      throw new Error('Error Getting the users, maybe the class name has changed? or some script is blocking the page')
    }
  }

  async scrollToEnd (usersContainer: ElementHandle<Element>): Promise<void> {
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
