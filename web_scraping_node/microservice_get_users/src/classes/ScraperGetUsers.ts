import puppeteer, { Browser, ElementHandle, Page } from 'puppeteer'
import { NODE_ENV_VALUES } from '@src/constants/env'
import { LoggerService as Logger } from '@src/classes/Logger'
import { Database } from '@src/classes/Database'
import { User } from '@src/interface/User'
import { joinClasses } from '@src/helpers/joinClasses.helper'
import { ELEMENT_CLASSES, HTML_ELEMENTS } from '@src/constants/classes.constant'

export class ScraperGetUsers {
  private _db: Database | undefined = undefined
  private readonly _logger: Logger = new Logger()

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
    console.log({ users })
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
        args:
          process.env.ENVIRONMENT === NODE_ENV_VALUES.PRODUCTION
            ? [
                '--no-sandbox',
                '--disable-extensions',
                '--lang=en',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--incognito'
              ]
            : ['--disable-extensions', '--lang=en']
      })
      const page = await browser.newPage()

      // Establish viewport size
      await page.setViewport({
        width: 1700,
        height: 800,
        deviceScaleFactor: 1,
        isMobile: false,
        hasTouch: false
      })

      return page
    } catch (err) {
      throw new Error('Error when launching browser')
    }
  }

  async login (page: Page): Promise<void> {
    try {
      await page.goto('https://www.instagram.com/accounts/login/')
      await page.waitForSelector('input[name="username"]')
      if (
        process.env.INSTAGRAM_USERNAME === undefined ||
        process.env.INSTAGRAM_PASSWORD === undefined
      ) {
        throw new Error('Instagram username or password is not defined')
      }
      await page.type('input[name="username"]', process.env.INSTAGRAM_USERNAME)
      if (process.env.INSTAGRAM_PASSWORD === undefined) {
        throw new Error('Instagram password is not defined')
      }
      await page.type('input[name="password"]', process.env.INSTAGRAM_PASSWORD)
      await page.click('button[type="submit"]')
      await page.waitForNavigation()
    } catch (err) {
      throw new Error('Error when logging in')
    }
  }

  async getUsers (page: Page): Promise<any[]> {
    try {
      if (process.env.INSTAGRAM_USERNAME === undefined) {
        throw new Error('Instagram username is not defined')
      }
      await page.goto(
        `https://www.instagram.com/${process.env.INSTAGRAM_USERNAME}/`
      )

      await new Promise((resolve) => setTimeout(resolve, 5000))

      const buttonFollowing = await page.waitForSelector(
        joinClasses(ELEMENT_CLASSES.BUTTON_FOLLOWING, HTML_ELEMENTS.ANCHOR),
        { timeout: 5000 }
      )
      if (buttonFollowing == null) {
        this._logger.errorLog(
          '❌ Button following not found, maybe the class name has changed?'
        )
        throw new Error('')
      }
      await buttonFollowing.click()
      const usersContainer = await page.waitForSelector(
        joinClasses(ELEMENT_CLASSES.CONTAINER_USERS, HTML_ELEMENTS.DIV),
        {
          timeout: 5000
        }
      )
      if (usersContainer == null) {
        this._logger.errorLog(
          '❌ Container following users not found, maybe the class name has changed?'
        )
        throw new Error('')
      }
      // Wait 5 seconds to ensure all users are loaded
      await new Promise((resolve) => setTimeout(resolve, 5000))
      await this.scrollToEnd(usersContainer)
      const usernameSpanClass = joinClasses(
        ELEMENT_CLASSES.USERNAME_SPAN,
        HTML_ELEMENTS.SPAN
      )
      const fullNameSpanClass = joinClasses(
        ELEMENT_CLASSES.FULLNAME_SPAN,
        HTML_ELEMENTS.SPAN
      )

      const users = await usersContainer.evaluate(
        (element, usersSpanClass, fullNameSpanClass) => {
          const usernameSpan = element.querySelectorAll(usersSpanClass)
          const fullNamesSpan = element.querySelectorAll(fullNameSpanClass)
          const usersStructured: User[] = []
          for (let i = 0; i < usernameSpan.length; i++) {
            const user: User = {
              username: usernameSpan[i].innerHTML ?? '',
              fullName: fullNamesSpan[i].innerHTML ?? ''
            }
            if (user.username !== '') {
              usersStructured.push(user)
              continue
            }
            this._logger.errorLog(
              `❌ User ${user.username} not added to the array because it is empty`
            )
          }
          return usersStructured
        },
        usernameSpanClass,
        fullNameSpanClass
      )
      return users
    } catch (err) {
      console.error(err)
      throw new Error(
        'Error Getting the users, maybe the class name has changed? or some script is blocking the page'
      )
    }
  }

  async scrollToEnd (usersContainer: ElementHandle<Element>): Promise<void> {
    console.log('Scroll To end', usersContainer)
    let previousHeight = 0
    let currentHeight = 0

    do {
      previousHeight = currentHeight
      await usersContainer.evaluate((element) => {
        element.scrollTop = element.scrollHeight
      })
      // Wait for 5 seconds to load the next users
      await new Promise((resolve) => setTimeout(resolve, 5000))

      currentHeight = await usersContainer.evaluate((element) => {
        return element.scrollHeight
      })
    } while (previousHeight < currentHeight)
  }
}
