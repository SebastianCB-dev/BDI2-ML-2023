import puppeteer, { Browser, ElementHandle, Page } from 'puppeteer'
import { NODE_ENV_VALUES } from '../constants/env'

export class ScraperFollowNewPeople {
  constructor () {}

  async run (): Promise<void> {
    const page = await this.launchBrowser()
    await this.login(page)
    await this.followNewPeople(page)
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

  async followNewPeople (page: Page): Promise<void> {
    try {
      await page.goto('https://www.instagram.com/explore/people/suggested/')
      await this.wait(5000)
      const buttons = await this.getButtonsFollow(page)
      for (const button of buttons) {
        await button.click()
        await this.wait(5000)
      }
    } catch (err) {
      console.error(err)
      throw new Error('Error following new users, maybe the class name has changed? or some script is blocking the page')
    }
  }

  async wait (ms: number): Promise<void> {
    return await new Promise((resolve) => setTimeout(resolve, ms))
  }

  async getButtonsFollow (page: Page): Promise<Array<ElementHandle<Element>>> {
    const buttons = await page.$$('._acan._acap._acas._aj1-._ap30')
    return buttons.filter(async (button) => {
      const text = await button.evaluate((node) => node.textContent)
      return text === 'Follow'
    })
  }
}
