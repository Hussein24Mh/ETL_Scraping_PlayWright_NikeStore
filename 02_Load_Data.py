import gspread
import pandas as pd

json_data_file = 'Data/Nike_Shoes.json'
spreadsheets_name = 'Nike_Shoes_PW_S'
work_sheet_name = 'Sheet1'

df = pd.read_json(json_data_file)


# Load Data to Google SpreadSheet File

sa = gspread.service_account(filename='Data/cloud-387509-0ba2461ed956.json')
sh = sa.open(spreadsheets_name)

try:
    wks = sh.worksheet(work_sheet_name)
except:
    wks = sh.add_worksheet(title=work_sheet_name, rows=100, cols=20)

wks.clear()

wks.update('', [df.columns.values.tolist()] + df.values.tolist())


# Load Data to CSV File

df.to_csv('Data/Jobs_CSV.csv', index=False)


# Load Data to Excel File

df.to_excel('Data/jobs_XLSX.xlsx')
