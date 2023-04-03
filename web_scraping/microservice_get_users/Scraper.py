# Standard libraries
import os
import time
import json

# Third-party libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

# Custom libraries
from helpers.platform import get_platform
from helpers.data_transform import deleteVerified, text_to_unicode
from services.users_service import UsersService


class Scraper:
    driver = None

    def __init__(self):
        # This function initializes the class
        self.setDriver()
        self.startDB()
        pass

    def startDB(self):
        # This function starts the database connection
        self.usersService = UsersService(os.getenv("DB_HOST"),
                                         os.getenv("DB_PORT"),
                                         os.getenv("DB_NAME"),
                                         os.getenv("DB_USER"),
                                         os.getenv("DB_PASSWORD"))

    def setDriver(self):
        # This function sets the driver for the browser
        platform = get_platform()
        service = None
        with open('./helpers/drivers.json') as f:
            drivers = json.load(f)
        if (drivers[platform] != None):
            service = Service(drivers[platform])
        else:
            Exception("No se reconoce el sistema operativo")
        self.driver = webdriver.Chrome(service=service)

    def getUsersFromInstagram(self):
        # This function gets all users that the account is following from Instagram
        self.driver.get("https://www.instagram.com/")
        # Login to Instagram fielding username and password
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.NAME, "username")
            )
        )
        username_field.send_keys(os.getenv("IG_USERNAME"))
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.NAME, "password")
            )
        )
        password_field.send_keys(os.getenv("IG_PASSWORD"))
        # Click on login button
        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit']")
            )
        )
        login_button.click()
        # Click on not now button
        try:
            not_now_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(text(), 'Not Now')]")
                )
            )
        except TimeoutException:
            not_now_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(), 'Not now')]")
                )
            )
        not_now_button.click()
        # Go to profile
        while(True):
          print('Go to profile')
          self.driver.get('https://www.instagram.com/' +
                          os.getenv('IG_USERNAME') + '/')
          print('Go to following')
          # Go to Following
          following_button = WebDriverWait(self.driver, 10).until(
              EC.presence_of_element_located(
                  (By.XPATH, "//a[contains(@href, '/following')]")
              )
          )
          following_button.click()
          # Get all users from box following
          time.sleep(2)
          print('Open modal')
          try:
              self.scroll_modal_users()
              # Get Usernames
              usernames = self.driver.execute_script(
                  "var elements = document.querySelectorAll('span._aacl._aaco._aacw._aacx._aad7._aade'); return Array.from(elements);")
              usernames = [username.text for username in usernames]
              usernames = usernames[1:]
              usernames = [deleteVerified(username) for username in usernames]            
              usernames = [text_to_unicode(username) for username in usernames]

              # Get Names
              # Get username and name
              names = self.driver.execute_script(
                  "var elements = document.querySelectorAll('span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj'); return Array.from(elements);")
              names = [name.text for name in names]
              names = [deleteVerified(name) for name in names]            
              names = [text_to_unicode(name) for name in names]            
              usernamesDB = self.usersService.getUsers()
              print('usernamesDB', usernamesDB)
              print(usernames)
              for username in usernames:
                  if (username not in usernamesDB):
                      self.usersService.createUser(username, names[usernames.index(username)])
              print('Añadidos a la base de datos')
              time.sleep(10)
          except Exception as e:
              print('error')
              print(e)

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
                "document.querySelector('._aano').scrollTop = "+str(scroll))
            height = int(self.driver.execute_script(
                "return document.querySelector('._aano').scrollTop"))
            new_height = height

            if (last_height == new_height):
                count = count + 1
            else:
                count = 0
            time.sleep(0.5)
            if (height >= scroll):
                scroll = scroll * height

            if (count > 2):
                # There is no more users
                break
