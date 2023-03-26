from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

service = Service('./drivers/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# abrir google.com
driver.get("https://www.google.com")

# buscar algo
search_box = driver.find_element(by='name', value='input')
search_box.send_keys("python")
search_box.send_keys(Keys.RETURN)

time.sleep(5000)