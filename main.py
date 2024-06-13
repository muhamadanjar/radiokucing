import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_presense():
	scope = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name(
		'add_json_file_here.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open('commentary data')
	sheet_instance = sheet.get_worksheet(0)

if __name__ == '__main__':
	print("init app")