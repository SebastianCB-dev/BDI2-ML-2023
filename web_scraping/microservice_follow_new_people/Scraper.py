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
from helpers.data_transform import deleteVerified, text_to_unicode
from helpers.platform import get_platform
from services.logging_service import LoggingService


class Scraper:
    # Public Properties
    driver = None
    logger = LoggingService().get_logging()

    def __init__(self):
        """Constructor
            This function initializes the class
            Set the driver 
        """
        self.set_driver()

    def get_logger(self):
        # This function returns the logger
        return self.logger

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
        if drivers[platform] != None:
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

    def follow_new_people(self):
        """Follow new People
            This function follows new people in Instagram
            It is necessary to be logged in to get the users.
            You have only to set the credentials in the .env file
        """
        self.driver.delete_all_cookies()
        # This function gets all users that the account is following from Instagram
        self.driver.get("https://www.instagram.com/")
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

        # Go to main page
        while True:
            self.driver.get("https://www.instagram.com/explore/people")
            time.sleep(3)
            try:
                wait = WebDriverWait(self.driver, 10)
                buttons = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "button._acan._acap._acas._aj1-")))
                print(buttons, len(buttons))
                for button in buttons:
                    try:
                        div = button.find_element(By.CSS_SELECTOR, 'div>div')
                        if div.text == 'Follow':
                            button.click()
                            time.sleep(2)
                    except Exception as e:
                        continue
                # Wait 2 minutes until next iteration to avoid being blocked
                time.sleep(120)
            except Exception as e:
                self.logger.error(f"Error: {e}")
                time.sleep(120)
                continue

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
