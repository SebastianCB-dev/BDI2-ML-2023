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
from services.logging_service import LoggingService


class Scraper:
    driver = None
    logger = LoggingService().getLogging()

    def __init__(self):
        # This function initializes the class
        self.setDriver()

    def getLogger(self):
        # This function returns the logger
        return self.logger

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
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.driver.maximize_window()

    def getUsersFromInstagram(self):
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
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
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

        # Go to main page
        while True:
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            # document.querySelectorAll('button._acan._acao._acas._aj1-') Get buttons
            try:
                wait = WebDriverWait(self.driver, 10)
                buttons = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "button._acan._acao._acas._aj1-")))
                print(buttons)
                for button in buttons:                  
                    try:
                        div = button.find_element(By.XPATH, ".//div[contains(text(), 'Follow')]")
                        print('Button found')
                        # button.click()
                        time.sleep(2)
                    except Exception as e:
                        continue
                # Wait 2 minutes until next iteration to avoid being blocked
                time.sleep(120)
            except Exception as e:
                self.logger.error(f"Error: {e}")
                time.sleep(120)
                continue

    def buscar_botones(self, driver, botones):
        for boton in botones:
            try:
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, boton))
                )
            except TimeoutException:
                continue
        raise TimeoutException("No se pudo encontrar ningún botón en la lista")
