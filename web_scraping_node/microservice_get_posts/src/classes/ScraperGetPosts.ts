import puppeteer, { Browser, ElementHandle, Page } from 'puppeteer'
import { NODE_ENV_VALUES } from '../constants/env'
import { Database } from './Database'
import { Logger } from '.'
import { UserPost } from '../interfaces'

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
    while (true) {
      const users = await this.getUsers()
      await this.getPosts(page, users)
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

  async getUsers (): Promise<string[]> {
    const usersDB: Array<Record<string, string>> = await this._db?.getUsers().then((res) => res.rows)
    if (!Array.isArray(usersDB) || usersDB.length === 0) {
      Logger.warningLog('⚠️ There are no users to get posts, please check the database.')
      return []
    }
    const users = usersDB.map((user) => user.username)
    return users
  }

  async getPosts (page: Page, users: string[]): Promise<void> {
    for (const user of users) {
      try {
        const urlUserProfile: string = `https://www.instagram.com/${'itssebastiancb'}/`
        await page.goto(urlUserProfile)
        const totalPosts: number = await this.getTotalPosts(page)
        if (totalPosts === 0) {
          Logger.warningLog(`⚠️ User ${user} has no posts`)
          await this.wait(1000)
          continue
        }
        const divPosts = await page.waitForSelector('.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > .x1iyjqo2', {
          timeout: 10000
        })
        if (divPosts == null) {
          Logger.errorLog('❌ Error when getting the divPosts, please check the selector of the divPosts')
          throw new Error('Error when getting the divPosts, Please check the selector of the divPosts')
        }
        const pageUser = await page.waitForSelector('html._9dls.js-focus-visible._aa4d')
        if (pageUser == null) {
          Logger.errorLog('❌ Error when getting the body, please check the selector of the body')
          throw new Error('Error when getting the body, Please check the selector of the body')
        }
        const posts = await this.scrollTrhoughPosts(pageUser, page)
        // Clean duplicated posts
        const postsNotRepeated = [...new Set(posts)]
        // Filter by https://www.instagram.com/p/
        const postRegex = /https:\/\/www.instagram.com\/p\//
        const postsFiltered = postsNotRepeated.filter((post) => postRegex.test(post))
        const userPosts: UserPost = {
          username: user,
          posts: postsFiltered
        }
        // TODO: Save the posts in the database
        console.log(userPosts.posts.length)
        // TODO: Put the user as REVIEWED in the database
        await this.wait(999999)
        // Slep 1 second to load the page
      } catch (err) {
        Logger.errorLog(`❌ Error when accessing the user profile: ${user}`)
        Logger.errorLog(err as string)
        await this.wait(1000)
        continue
      }
      await this.wait(1000)
    }
    // const commentsNotRepeated = [...new Set(comments)]
    await new Promise((resolve) => setTimeout(resolve, 180000))
  }

  async getTotalPosts (page: Page): Promise<number> {
    const spansUserInfo = await page.waitForSelector('.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs', {
      timeout: 10000
    })
    if (spansUserInfo == null) {
      Logger.errorLog('❌ Error when getting the total number of posts, please check the selector of the spansUserInfo')
      throw new Error('Error when getting the total number of posts, Please check the selector of the spansUserInfo')
    }

    const spansUserInfoText = await page.evaluate((elem) => elem.textContent, spansUserInfo)
    if (spansUserInfoText == null) {
      Logger.errorLog('❌ Error when getting the total number of posts, please check the selector of the spansUserInfoText')
      throw new Error('Error when getting the total number of posts, Please check the selector of the spansUserInfoText')
    }
    return parseInt(spansUserInfoText)
  }

  async wait (ms: number): Promise<void> {
    return await new Promise((resolve) => setTimeout(resolve, ms))
  }

  async scrollTrhoughPosts (usersPosts: ElementHandle<Element>, page: Page): Promise<string[]> {
    let previousHeight = 0
    let currentHeight = 0
    const posts: string[] = []
    do {
      const newPosts = await this.getPostsByDiv(page, usersPosts)
      posts.push(...newPosts)
      previousHeight = currentHeight
      await usersPosts.evaluate((element) => {
        element.scrollTop = element.scrollHeight
      })
      // Wait for 3 seconds to load the next users
      await new Promise(resolve => setTimeout(resolve, 3000))

      currentHeight = await usersPosts.evaluate((element) => {
        return element.scrollHeight
      })
    } while (previousHeight < currentHeight)
    return posts
  }

  async getPostsByDiv (page: Page, divPosts: ElementHandle<Element>): Promise<string[]> {
    const posts = await page.evaluate((elem) => {
      const imgs = elem?.querySelectorAll<HTMLLinkElement>('.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._a6hd')
      const postUrls: string[] = []
      imgs?.forEach((img) => postUrls.push(img?.href ?? ''))
      return postUrls
    }, divPosts)
    return posts
  }
}
