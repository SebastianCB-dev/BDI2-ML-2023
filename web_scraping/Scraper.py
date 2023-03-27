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
from selenium.webdriver.support.ui import WebDriverWait

# Custom libraries
from helpers.platform import get_platform


class Scraper:
  driver = None

  def __init__(self):
    self.setDriver()
    pass

  def setDriver(self):
    platform = get_platform()
    service = None
    with open('example.json') as f:
        drivers = json.load(f)
    if(drivers[platform] != None):
      service = Service(drivers[platform])
    else:
      Exception("No se reconoce el sistema operativo")    
    self.driver = webdriver.Chrome(service=service)

  def getUsersFromInstagram(self):
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
    not_now_button = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located(
        (By.XPATH, "//button[contains(text(), 'Not Now')]")
      )
    )
    not_now_button.click()
    # Go to profile
    profile_button = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href, '/" + os.getenv("IG_USERNAME") + "/')]")
      )
    )
    profile_button.click()
    # Go to followers
    followers_button = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href, '/" + os.getenv("IG_USERNAME") + "/followers')]")
        )
    )
    followers_button.click()

    time.sleep(10)
