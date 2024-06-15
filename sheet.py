
from __future__ import print_function
from auth import spreadsheet_service
from auth import drive_service, credentials
import os
import requests
from urllib.parse import urlencode
from datetime import date
import gspread
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


def create():
	spreadsheet_details = {
		'properties': {
			'title': 'Python-google-sheets-demo'
		}
    }

	sheet = spreadsheet_service.spreadsheets().create(body=spreadsheet_details,
                                                   fields='spreadsheetId').execute()

	sheetId = sheet.get('spreadsheetId')
	print('Spreadsheet ID: {0}'.format(sheetId))
	permission1 = {
		'type': 'user',
		'role': 'writer',
		'emailAddress': 'arvanria@gmail.com'
    }
	drive_service.permissions().create(fileId=sheetId, body=permission1).execute()
	return sheetId


def read_range():
    range_name = 'Sheet1!A1:H1'
    spreadsheet_id = '1JCEHwIa4ZzwAiKGmAnWGfbjeVCH_tWZF6MkIU0zICwM'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    print('{0} rows retrieved.'.format(len(rows)))
    print('{0} rows retrieved.'.format(rows))
    return rows


def write_range():
    spreadsheet_id = create()
    range_name = 'Sheet1!A1:H1'
    values = read_range()
    value_input_option = 'USER_ENTERED'
    body = {
        'values': values
    }
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def read_ranges():
    write_range()
    sheetId = '1JCEHwIa4ZzwAiKGmAnWGfbjeVCH_tWZF6MkIU0zICwM'
    range_names = ['Sheet1!A2:H21', 'Sheet1!A42:H62']
    result = spreadsheet_service.spreadsheets().values().batchGet(
        spreadsheetId=sheetId, ranges=range_names).execute()
    ranges = result.get('valueRanges', [])
    print('{0} ranges retrieved.'.format(len(ranges)))
    return ranges


def write_ranges():
    values = read_ranges()
    data = [
        {
            'range': 'Sheet1!A2:H21',
            'values': values[0]['values']
        },
        {
            'range': 'Sheet1!A22:H42',
            'values': values[1]['values']
        }
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    result = spreadsheet_service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


def prepare_token():
	base_url = "https://api-open.olsera.co.id/api/open-api/v1/"
	app_id = os.environ.get("APP_ID")
	secret_key = os.environ.get("SECRET_KEY")
	payload = {
		"app_id": app_id,
		"secret_key": secret_key,
		"grant_type": "secret_key"
	}
	response = requests.post(f"{base_url}id/token", data=payload)
	return response.json()

def presense():
	base_url = "https://api-open.olsera.co.id/api/open-api/v1/"
	auth_data = {}
	if not auth_data:
		auth_data = prepare_token()

	access_token = auth_data['access_token']
	headers = {'Authorization': f'Bearer {access_token}'}
	data_request = {
		'start_date': date.today(), 
		'end_date': date.today(),
		# 'start_date': '2024-06-15',
		# 'end_date': '2024-06-15'
	}

	qs = urlencode(data_request)

	print("date", date.today())

	response = requests.get(f"{base_url}en/attendance/presence?{qs}", headers=headers)
	presense_data = response.json()
	# print(presense_data)

	keys_list = [list(entry.keys()) for entry in presense_data['data']]
	headers = list(set().union(*keys_list))
	# print("header", headers)
	spreadsheet_id = os.environ.get("SHEET_ID")

	client = gspread.authorize(credentials)
	workbook = client.open_by_key(spreadsheet_id)

	worksheet_list = list(map(lambda x: x.title, workbook.worksheets()))
	worksheet_name = "Absensi"
	if worksheet_name in worksheet_list:
		sheet = workbook.worksheet(worksheet_name)
	else:
		sheet = workbook.add_worksheet(worksheet_name, rows=10, cols=10)

	sheet.clear()

	col_num = 2
	sheet.update_acell(f"A{col_num}", 'Nama Karyawan')
	sheet.update_acell(f"B{col_num}", 'Kode Karyawan')
	sheet.update_acell(f"C{col_num}", 'Tanggal')
	sheet.update_acell(f"D{col_num}", 'Jam Datang')
	sheet.update_acell(f"E{col_num}", 'Jam Pulang')
	sheet.update_acell(f"F{col_num}", 'Total Jam')
	for presense in presense_data['data']:
		col_num += 1
		sheet.update_acell(f"A{col_num}", presense['employee_name'])
		sheet.update_acell(f"B{col_num}", presense['employee_id'])
		sheet.update_acell(f"C{col_num}", presense['fdate'])
		sheet.update_acell(f"D{col_num}", presense['time_coming'])
		sheet.update_acell(f"E{col_num}", presense['time_going'])
		sheet.update_acell(f"F{col_num}", presense['fduration'])

presense()
