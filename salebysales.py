from load_env import *
from utils.scrape_service import driver, time, By, EC, wait
import gspread
from auth import credentials

salesman = ['AMEL', 'IRSYAD', 'RIAN', 'WIDIA', 'WIWI']


spreadsheet_id = get_env("SHEET_ID")
client = gspread.authorize(credentials)
workbook = client.open_by_key(spreadsheet_id)

sheet = workbook.worksheet("DASHBOARD")

def update_cell(report_item):
	report_item_button = report_item.find_element(By.CSS_SELECTOR, 'button')

	report_item_button_text = (report_item_button.find_element(By.TAG_NAME, 'h4').get_attribute("innerHTML")).upper()

	print(report_item_button_text)
	if report_item_button_text in salesman:
		report_item_button.click()

		time.sleep(10)

		summary = report_items = wait.until(EC.visibility_of_element_located(
			(By.CSS_SELECTOR, '.summary')))

		# table = summary.get_attribute("innerHTML")
		# print("table",summary.get_attribute("innerHTML"))

		contents = summary.find_elements(By.CSS_SELECTOR, 'table tbody tr')
		for content in contents:
			td = content.find_elements(By.TAG_NAME, 'td')
			for idx, tdv in enumerate(td):
				if idx == 2:
					val = int(tdv.get_attribute("innerHTML").replace("IDR ", "").replace(".", ""))
					print(val)
					if report_item_button_text == "IRSYAD":
						sheet.update_acell(f"N5", val)
		time.sleep(2)
		# driver.find_element(By.CSS_SELECTOR, 'button.el-button.el-icon-back').click()


driver.get("https://dashboard.olsera.co.id/reports/sales?path=salesbysalesman")
wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.content-wrapper')))


report_page = driver.find_element(By.CSS_SELECTOR, '.report-page')


report_items = wait.until(EC.visibility_of_all_elements_located(
    (By.CSS_SELECTOR, '.report-item')))

# print("report item", report_items)

idx = 0
total_report = len(report_items)

for report_index in range(total_report):
	report_item = report_items[report_index]
	idx = report_index
	update_cell(report_item)
	

time.sleep(5)

driver.quit()

