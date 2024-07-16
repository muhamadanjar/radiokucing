
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from load_env import *
import time

service = Service(excecute_path="chromedriver")

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)
driver.get("https://dashboard.olsera.co.id")
rk_email = get_env("EMAIL")
rk_password = os.environ.get("PASSWORD")

email_element = driver.find_element(
    By.CSS_SELECTOR, "input[placeholder='Email']")
email_element.send_keys(rk_email)

password_element = driver.find_element(
    By.CSS_SELECTOR, "input[placeholder='Password']")
password_element.send_keys(rk_password)

password_element.send_keys(Keys.ENTER)


wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.login-banner--card')))

button = driver.find_element(By.CSS_SELECTOR, '.login-banner--card')
button.click()


time.sleep(3)

