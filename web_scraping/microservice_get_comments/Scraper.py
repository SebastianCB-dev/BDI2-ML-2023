# Standard libraries
import os
import time
import json

# Third-party libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

# Custom libraries
from helpers.platform import get_platform
from helpers.data_transform import deleteVerified, text_to_unicode
from services.database_service import DatabaseService
from services.logging_service import LoggingService


class Scraper:
    # Public Properties
    driver = None
    logger = LoggingService().getLogging()
    databaseService = None

    def __init__(self):
        """Constructor
            This function initializes the class
            Set the driver and connect to the database
        """
        self.setDriver()
        self.startDB()

    def getLogger(self):
        # This function returns the logger
        return self.logger

    def startDB(self):
        """Database
            This function starts the database connection
            * Set variables from .env file
        """
        self.databaseService = DatabaseService(os.getenv('POSTGRES_URL'))
        self.logger.info("Database connection started")

    def setDriver(self):
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
        # If the operating system is Linux, then set the options
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
        """Get Comments From Instagram
            This function gets all the comments from a post that the account follows
            It is necessary to be logged in to get the users.
            You have only to set the credentials in the .env file
        """
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
        # Loop to get the next user every 20 seconds
        while True:
            # Get 4 posts with status PENDING
            posts = self.databaseService.get_posts()
            print(posts)
            for post in posts:
                self.driver.get(post)
                comments = self.scroll_comments()
                print(comments)
                # Save comments in database
                for comment in comments:
                    self.databaseService.create_comment(comment)
                # Update user status to DONE
                self.databaseService.set_post_done(post)
            time.sleep(20)

    def buscar_botones(self, driver, botones):
        # This function search for buttons in a list of XPATH
        for boton in botones:
            try:
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, boton))
                )
            except TimeoutException:
                continue
        raise TimeoutException("No se pudo encontrar ningún botón en la lista")

    def scroll_comments(self):
        """Scroll Comments
            This function scrolls the comments of a post
            It is necessary to click on the button "View all comments" to get all the comments
        """
        scroll = 400
        height = 0
        last_height = 0
        new_height = 10
        count = 0
        general_comments = []
        while True:
            time.sleep(3)
            try:
                self.clickReplyComments()
            except Exception as e:
                self.logger.error(e)
                pass
            general_new_comments = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class, '_a9zr')]"))
            )
            general_comments.extend(general_new_comments)
            if len(general_comments) == 0:
                self.logger.info(
                    f"No comments found for this post {self.driver.current_url}")
                break
            # Get Comments
            comments_processed = self.process_comments(general_comments)
            # Delete duplicate
            comments = list(set(tuple(comment.items())
                            for comment in comments_processed))
            comments = [dict(comment) for comment in comments]
            try:
                self.clickButtonMoreComments()
            except:
                pass

            last_height = height
            self.driver.execute_script(
                "document.querySelector('ul._a9z6._a9za').scrollTop = " + str(
                    scroll))
            height = int(self.driver.execute_script(
                "return document.querySelector('ul._a9z6._a9za').scrollTop"))
            new_height = height
            try:
                self.clickButtonMoreComments()
            except:
                pass
            time.sleep(3)
            if last_height == new_height:
                count = count + 1
            else:
                count = 0
            time.sleep(1)
            if height >= scroll:
                scroll = scroll * height

            if count > 2:
                try:
                    self.clickButtonMoreComments()
                    time.sleep(3)
                except NoSuchElementException:
                    break
                except Exception as e:
                    break

            return comments

    def process_comments(self, general_comments):
        """Process Comments
            This function process the comments of a post            
        """
        comments = []
        for gc in general_comments:
            source = gc.get_attribute('innerHTML')
            soup = BeautifulSoup(source, "html.parser")
            text = soup.find(
                "span", {"class": "_aacl _aaco _aacu _aacx _aad7 _aade"})
            username = soup.find("a")
            username = username.text
            print(username)
            username = deleteVerified(username)
            if text is None:
                text = soup.find(
                    "h1", {"class": "_aacl _aaco _aacu _aacx _aad7 _aade"})
            text = text.text
            text = text_to_unicode(text)
            comment_object = {"text": text, "username": username}
            comments.append(comment_object)

        return comments

    def clickButtonMoreComments(self):
        """Click Button More Comments
            This function clicks on the button "View all comments" to get all the comments
        """
        script = """
        var div_more_comments = document.querySelector("div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xdj266r.xat24cr.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.xl56j7k");
        var button_more_comments = div_more_comments.querySelector("button");
        button_more_comments.click();
        """

        # Execute script
        self.driver.execute_script(script)

    def clickReplyComments(self):
        """Click Reply Comments
            This function clicks on the button "View replies" to get all the replies
        """
        buttons = self.driver.find_elements(
            By.CSS_SELECTOR, value='button._acan._acao._acas._aj1-')
        for button in buttons:
            span_element = button.find_element(By.XPATH,
                                               ".//span[contains(text(), 'View replies')]")
            if (span_element is not None):
                button.click()
            time.sleep(2)
