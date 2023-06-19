# Standard libraries
import json
import os
import time

# Third-party libraries
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Custom libraries
from helpers.platform import get_platform, is_darwin_arm_validator
from services.database_service import DatabaseService
from services.logging_service import LoggingService


class Scraper:
    # Public Properties
    driver = None
    logger = LoggingService().get_logging()
    databaseService = None

    def __init__(self):
        """Constructor
            This function initializes the class
            Set the driver and connect to the database
        """
        self.set_driver()
        self.start_db()

    def getLogger(self):
        # This function returns the logger
        return self.logger

    def start_db(self):
        """Database
            This function starts the database connection
            * Set variables from .env file
        """
        self.databaseService = DatabaseService(os.getenv('POSTGRES_URL'))
        self.logger.info("Database connection started")

    def set_driver(self):
        """Driver
            This function sets the driver
            The driver allows to use the browser and navigate through the web            
        """
        # get_platform() returns the operating system
        platform = get_platform()
        is_darwin_arm = is_darwin_arm_validator()
        if (platform == "Darwin" and is_darwin_arm):
            platform = "Darwin_ARM"
        driver_path = None
        # Load the drivers' paths from the json file
        with open("./helpers/drivers.json") as f:
            drivers = json.load(f)
        if drivers[platform] is not None:
            self.logger.info(f"Driver found to {platform}")
            driver_path = drivers[platform]
        else:
            self.logger.error("Could not recognize the operating system")
            Exception("Could not recognize the operating system")
        options = Options()
        if (platform != "Windows"):
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--incognito')
        options.add_argument("--disable-extensions")
        options.add_argument("--lang=en")
        # If the operating system is Linux, then set the options
        self.driver = webdriver.Chrome(
            executable_path=driver_path, options=options)

    def get_posts_from_instagram(self):
        """Get Posts From Instagram
            This function gets all posts from Instagram that the account follows
            It is necessary to be logged in to get the posts.
            You have only to set the credentials in the .env file
        """
        self.driver.delete_all_cookies()
        # This function gets all users that the account is following from Instagram
        self.driver.get("https://www.instagram.com/accounts/login?hl=en")
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
        xpath_buttons_not_now = [
            "//button[contains(text(), 'Not Now')]",
            "//div[contains(text(), 'Not Now')]",
            "//span[contains(text(), 'Not Now')]",
            "//div[contains(text(), 'Not now')]",
        ]
        not_now_button = self.search_buttons(
            self.driver, xpath_buttons_not_now)
        not_now_button.click()

        while True:
            # Get 4 users with status PENDING
            users = self.databaseService.get_users()
            for user in users:
                self.driver.get("https://www.instagram.com/" + user)
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
                # Update user status to DONE
                self.databaseService.set_done_user(user)
                time.sleep(20)

    def search_buttons(self, driver, buttons_path):
        # This function search for buttons in a list of XPATH
        for boton in buttons_path:
            try:
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, boton))
                )
            except TimeoutException:
                continue
        raise TimeoutException("There is no any button in the list")
