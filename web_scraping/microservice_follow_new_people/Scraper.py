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
# from helpers.data_transform import deleteVerified, text_to_unicode
# from services.users_service import UsersService
# from services.logging_service import LoggingService


class Scraper:
    driver = None
    logger = LoggingService().getLogging()

    def __init__(self):
        # This function initializes the class
        self.setDriver()
        self.startDB()

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
        options = webdriver.ChromeOptions()
        if (platform == "Windows"):
            self.driver = webdriver.Chrome(executable_path=driver_path)
            self.driver.maximize_window()
            return
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(
            executable_path=driver_path, options=options)
        self.driver.maximize_window()

    def getUsersFromInstagram(self):
      pass
