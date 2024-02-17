import gspread
from sheet import GSheet

a = GSheet()
a.auth_user() #authenticate the user
a.open_google_sheet(sheet_id="1PKDskq94WwKit6KmVFyop1fZ2yi0eHQoAVYOg7k6JpI")
a.test_func()

