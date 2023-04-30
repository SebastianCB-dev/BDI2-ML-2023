# Standard libraries
import os
import time
import json

# Third-party libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

# Custom libraries
from helpers.platform import get_platform
from helpers.data_transform import deleteVerified, text_to_unicode
from services.database_service import DatabaseService
from services.logging_service import LoggingService


class Scraper:
    driver = None
    logger = LoggingService().getLogging()
    databaseService = None

    def __init__(self):
        # This function initializes the class
        self.setDriver()
        self.startDB()

    def getLogger(self):
        # This function returns the logger
        return self.logger

    def startDB(self):
        # This function starts the database connection
        self.databaseService = DatabaseService(
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
        if drivers[platform] is not None:
            self.logger.info(f"Driver found to {platform}")
            driver_path = drivers[platform]
        else:
            self.logger.error("Don't recognize the operating system")
            Exception("Don't recognize the operating system")
        if platform == "Windows":
            self.driver = webdriver.Chrome(executable_path=driver_path)
            self.driver.maximize_window()
            return
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(
            executable_path=driver_path, options=options)
        self.driver.maximize_window()

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
            # Get 4 users with status PENDING
            users = self.databaseService.get_users()
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
                        "const posts_urls = []; document.querySelectorAll('div._aabd._aa8k._al3l').forEach(post => "
                        "posts_urls.push('https://instagram.com' + post.querySelector('a').getAttribute('href'))); "
                        "return posts_urls")
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
                # Save Posts in database
                for post in posts_urls:
                    self.databaseService.create_post(post, user)            
                time.sleep(20)

    def buscar_botones(self, driver, botones):
        # This function searches for buttons in the page
        for boton in botones:
            try:
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, boton))
                )
            except TimeoutException:
                continue
        raise TimeoutException("No se pudo encontrar ningún botón en la lista")
