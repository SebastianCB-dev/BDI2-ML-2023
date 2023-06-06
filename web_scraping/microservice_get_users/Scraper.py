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
from helpers.data_transform import delete_verified, text_to_unicode
from services.users_service import UsersService
from services.logging_service import LoggingService


class Scraper:
    # Public Properties
    driver = None
    logger = LoggingService().get_logging()

    def __init__(self):
        """Constructor
            This function initializes the class
            Set the driver and connect to the database
        """
        self.set_driver()
        self.start_database()

    def get_logger(self):
        # This function returns the logger
        return self.logger

    def start_database(self):
        """Database
            This function starts the database connection
            * Set variables from .env file
        """
        self.users_service = UsersService(os.getenv('POSTGRES_URL'))
        self.logger.info("Database connection started")

    def set_driver(self):
        """Driver
            This function sets the driver
            The driver allows to use the browser and navigate through the web            
        """
        # get_platform() returns the operating system
        platform = get_platform()
        driver_path = None
        # Load the drivers' paths from the json file
        with open("./helpers/drivers.json") as f:
            drivers = json.load(f)
        if drivers[platform] != None:
            self.logger.info(f"Driver found to {platform}")
            driver_path = drivers[platform]
        else:
            self.logger.error("Don't recognize the operating system")
            Exception("Don't recognize the operating system")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--lang=en")
        if (platform != "Windows"):
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--incognito')            
        # If the operating system is Linux, then set the options
       
        self.driver = webdriver.Chrome(
            executable_path=driver_path, options=options)
        self.driver.maximize_window()

    def get_users(self):
        """Get Users From Instagram
            This function gets all users from Instagram that the account follows
            It is necessary to be logged in to get the users.
            You have only to set the credentials in the .env file
        """
        self.driver.delete_all_cookies()
        # Open Instagram with English language
        self.driver.get("https://www.instagram.com/?hl=en")
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
        not_now_button = self.search_buttons(self.driver, xpath_buttons_not_now)
        not_now_button.click()

        # Go to profile
        # Loop to get all users from following list every 2 minutes
        while True:
            self.logger.info("Going to profile")
            self.driver.get(
                "https://www.instagram.com/" + os.getenv("IG_USERNAME") + "/"
            )
            # Go to Following
            following_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@href, '/following')]")
                )
            )
            following_button.click()
            # Get all users from box following
            time.sleep(2)
            self.logger.info("Opening modal to get users")
            try:
                self.scroll_modal_users()
                # Get Usernames
                usernames = self.driver.execute_script(
                    "var elements = document.querySelectorAll('span._aacl._aaco._aacw._aacx._aad7._aade'); return Array.from(elements);"
                )
                usernames = [username.text for username in usernames]
                usernames = usernames[1:]
                usernames = [delete_verified(username)
                             for username in usernames]
                usernames = [text_to_unicode(username)
                             for username in usernames]

                # Get Names
                # Get username and name
                names = self.driver.execute_script(
                    "var elements = document.querySelectorAll('span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj'); return Array.from(elements);"
                )
                names = [name.text for name in names]
                names = [delete_verified(name) for name in names]
                names = [text_to_unicode(name) for name in names]
                usernames_database = self.users_service.get_users()
                # Add users to database
                for username in usernames:
                    if username not in usernames_database:
                        self.users_service.create_user(
                            username, names[usernames.index(username)]
                        )
                self.logger.info("Users added to database")
                # Timer to repeat the process every 2 minutes and avoid being blocked
                time.sleep(120)
            except Exception as e:
                self.logger.error(f"Error getting users {e.__str__()}")
                time.sleep(120)

    def scroll_modal_users(self):
        # This function scrolls the modal to get all users
        scroll = 500
        height = 0
        last_height = 0
        new_height = 10
        count = 0
        while True:
            last_height = height
            self.driver.execute_script(
                "document.querySelector('._aano').scrollTop = " + str(scroll)
            )
            height = int(
                self.driver.execute_script(
                    "return document.querySelector('._aano').scrollTop"
                )
            )
            new_height = height

            if last_height == new_height:
                count = count + 1
            else:
                count = 0
            time.sleep(0.5)
            if height >= scroll:
                scroll = scroll * height

            if count > 2:
                # There is no more users
                break

    def search_buttons(self, driver, buttons):
        # This function search for buttons in a list of XPATH
        for button in buttons:
            try:
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, button))
                )
            except TimeoutException:
                continue
        raise TimeoutException("There is no any button in the list")
