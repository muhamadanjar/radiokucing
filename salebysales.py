from load_env import *
from utils.scrape_service import driver, time, By, EC, wait
import gspread
from auth import credentials


driver.get("https://dashboard.olsera.co.id/reports/sales?path=salesbysalesman")
wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.content-wrapper')))


report_page = driver.find_element(By.CSS_SELECTOR, '.report-page')

report_item = wait.until(EC.visibility_of_all_elements_located(
    (By.CSS_SELECTOR, '.report-item')))

print("report item", report_item)


spreadsheet_id = get_env("SHEET_ID")
client = gspread.authorize(credentials)
workbook = client.open_by_key(spreadsheet_id)

sheet = workbook.worksheet("DASHBOARD")


for item in report_item:
	summary = item.find_element(By.CLASS_NAME, 'summary')
	summary_val = summary.get_attribute('innerHTML')
	sheet.update_acell(f"M9", summary_val)

time.sleep(5)

driver.quit()
