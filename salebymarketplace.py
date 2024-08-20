from load_env import *
from utils.scrape_service import driver, time, By, EC, wait
import gspread
from auth import credentials
from datetime import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("date")
args = parser.parse_args()

current_date = args.date

date_now = datetime.strptime(current_date, "%Y-%m-%d")


spreadsheet_id = get_env("SHEET_ID")
client = gspread.authorize(credentials)
workbook = client.open_by_key(spreadsheet_id)
sheet = workbook.worksheet("DASHBOARD")

driver.get(
    "https://dashboard.olsera.co.id/reports/sales?path=salesdetailsmarketplace")



wrapper = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.content-wrapper')))

date_picker_wrapper = wrapper.find_element(By.CSS_SELECTOR, '.date-range-picker-wrapper')
date_picker_wrapper.click()


time.sleep(5)
daterangepicker = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.daterangepicker')))
if daterangepicker:
	daterangepicker.find_element(By.CSS_SELECTOR, '[data-range-key="Today"]').click()

time.sleep(5)



summary = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.summary')))
table_contents = summary.find_elements(By.CSS_SELECTOR, 'table tbody tr')
start_column = 3
for content in table_contents:
	td = content.find_elements(By.TAG_NAME, 'td')
	for idx, tdv in enumerate(td):
		if idx == 6:
			val = int(tdv.get_attribute("innerHTML").replace(
                    "IDR ", "").replace(".", ""))
			print(val)
			day = start_column + int(date_now.day)
			print(f"H{day}")
			sheet.update_acell(f"H{day}", val)
		
time.sleep(5)
driver.quit()
