# Standard libraries
import os
import time
import json

# Third-party libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

# Custom libraries
from helpers.platform import get_platform
from helpers.data_transform import deleteVerified, text_to_unicode
from services.users_service import UsersService
from services.logging_service import LoggingService


class Scraper:
    driver = None
    logger = LoggingService().getLogging()

    def __init__(self):
        # This function initializes the class
        self.setDriver()
        # self.startDB()

    def getLogger(self):
        # This function returns the logger
        return self.logger

    def startDB(self):
        # This function starts the database connection
        self.usersService = UsersService(
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
        )
        self.logger.info("Database connection started")

    def setDriver(self):
        # This function sets the driver for the browser
        platform = get_platform()
        driver_path = None
        with open("./helpers/drivers.json") as f:
            drivers = json.load(f)
        if drivers[platform] != None:
            self.logger.info(f"Driver found to {platform}")
            driver_path = drivers[platform]
        else:
            self.logger.error("Don't recognize the operating system")
            Exception("Don't recognize the operating system")
        if (platform == "Windows"):
            self.driver = webdriver.Chrome(executable_path=driver_path)
            return
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(
            executable_path=driver_path, options=options)

    def getCommentsFromInstagram(self):
        self.driver.delete_all_cookies()
        # This function gets all users that the account is following from Instagram
        self.driver.get("https://www.instagram.com/accounts/login")
        # Login to Instagram fielding username and password
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys(os.getenv("IG_USERNAME"))
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(os.getenv("IG_PASSWORD"))
        # Click on login button
        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()
        # Click on not now button
        botones = [
            "//button[contains(text(), 'Not Now')]",
            "//div[contains(text(), 'Not Now')]",
            "//span[contains(text(), 'Not Now')]",
            "//div[contains(text(), 'Not now')]",
        ]
        not_now_button = self.buscar_botones(self.driver, botones)
        not_now_button.click()

        while True:
            # TODO: Get From Database 10 in PENDING STATUS
            users = ['lesliedayana97']
            for user in users:
                self.driver.get('https://www.instagram.com/' + user)
                SCROLL_PAUSE_TIME = 3
                posts_urls = []
                while True:
                    # Get scroll height
                    # This is the difference. Moving this *inside* the loop
                    # means that it checks if scrollTo is still scrolling
                    last_height = self.driver.execute_script(
                        "return document.body.scrollHeight")
                    # print(last_height)
                    # Scroll down to bottom
                    self.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)
                    # Calculate new scroll height and compare with last scroll height
                    new_height = self.driver.execute_script(
                        "return document.body.scrollHeight")
                    new_posts = self.driver.execute_script(
                        "const posts_urls = []; document.querySelectorAll('div._aabd._aa8k._al3l').forEach(post => posts_urls.push('https://instagram.com' + post.querySelector('a').getAttribute('href'))); return posts_urls")
                    posts_urls.extend(new_posts)
                    if new_height == last_height:

                        # try again (can be removed)
                        self.driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")

                        # Wait to load page
                        time.sleep(SCROLL_PAUSE_TIME)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = self.driver.execute_script(
                            "return document.body.scrollHeight")

                        # check if the page height has remained the same
                        if new_height == last_height:
                            # if so, you are done
                            break
                        # if not, move on to the next loop
                        else:
                            last_height = new_height
                            continue
                # Posts URLS
                # Delete duplicated
                posts_urls = list(set(posts_urls))
                print(len(posts_urls))
                time.sleep(2000)
                for post in posts_urls:
                    self.driver.get(post)
                    description = self.get_publication_description()
                    print(description)
                    comments = self.scroll_comments()
                    time.sleep(20)

    def buscar_botones(self, driver, botones):
        for boton in botones:
            try:
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, boton))
                )
            except TimeoutException:
                continue
        raise TimeoutException("No se pudo encontrar ningún botón en la lista")

    def get_publication_description(self):
        try:
            description_post_h1 = username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1"))
            )
            return description_post_h1.text
        except Exception:
            # If publication does not have a description return empty string
            return ''
        

    def scroll_comments(self):
        return ''
        
