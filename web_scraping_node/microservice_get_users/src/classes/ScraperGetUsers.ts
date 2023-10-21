import puppeteer, { Browser, Page } from 'puppeteer'
import { NODE_ENV_VALUES } from '../constants/env'
import { Logger } from './Logger'

export class ScraperGetUsers {
  /**
   * Start the web scraper to get the users from Instagram.
   * @returns {Promise<void>}
   */
  async run (): Promise<void> {
    const page = await this.launchBrowser()
    await this.login(page)
    await this.getUsers(page)
  }

  async launchBrowser (): Promise<Page> {
    try {
      const browser: Browser = await puppeteer.launch({
        headless: process.env.ENVIRONMENT === NODE_ENV_VALUES.PRODUCTION,
        args: process.env.ENVIRONMENT === NODE_ENV_VALUES.PRODUCTION
          ? ['--no-sandbox', '--disable-extensions', '--lang=en', '--disable-dev-shm-usage', '--disable-gpu', '--incognito']
          : ['--disable-extensions', '--lang=en']
      })
      const page: Page = await browser.newPage()
      return page
    } catch (err) {
      throw new Error('Error when launching browser')
    }
  }

  async login (page: Page): Promise<void> {
    try {
      await page.goto('https://www.instagram.com/accounts/login/')
      await page.waitForSelector('input[name="username"]')
      await page.type('input[name="username"]', process.env.INSTAGRAM_USERNAME as string)
      await page.type('input[name="password"]', process.env.INSTAGRAM_PASSWORD as string)
      await page.click('button[type="submit"]')
      await page.waitForNavigation()
    } catch (err) {
      throw new Error('Error when logging in')
    }
  }

  async getUsers (page: Page): Promise<void> {
    try {
      await page.goto(`https://www.instagram.com/${process.env.INSTAGRAM_USERNAME}/following/`)
    } catch (err) {
      throw new Error('Error when going to the account`s following users')
    }
  }
}
