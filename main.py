from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

rk_email = os.environ.get("EMAIL")
rk_password = os.environ.get("PASSWORD")

service = Service(excecute_path="chromedriver")

driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 10)
driver.get("https://dashboard.olsera.co.id")

email_element = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Email']")
email_element.send_keys(rk_email)

password_element = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
password_element.send_keys(rk_password)

password_element.send_keys(Keys.ENTER)


wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.login-banner--card')))

button = driver.find_element(By.CSS_SELECTOR, '.login-banner--card')
button.click()


time.sleep(3)

driver.get("https://dashboard.olsera.co.id/reports/sales?path=salesbysalesman")

wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.content-wrapper')))
container = driver.find_element(By.CSS_SELECTOR, '.content-wrapper')
container.find_element(By.CSS_SELECTOR, '.el-icon-document').click()


time.sleep(10)
driver.quit()
