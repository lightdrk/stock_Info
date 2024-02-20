import json
import gspread

class GSheet:
    ''' custom class for google sheet '''
    def __init__(self, sheet_id=None):
        self.open = None
        self.id = sheet_id
        self.gc = None
        self.creds = None
        self.authorized_user = None
        self.enter_worksheet = None
        self.image_path = './image_output'
        self.path_to_client = './creds/client_secret.json'
        self.path_to_auth = './creds/authorized_user.json'

    def explicity_new_auth(self):
        '''authenticate explicity '''
        try:
            self.gc = gspread.oauth(
                        credentials_filename = self.path_to_client,
                        authorized_user_filename = self.path_to_auth
                    )

        except Exception as err:
            print(f'failed new authentication due: {err}')

        return 1 if self.gc else 0

    def auth_user(self):
        '''
            authenticate user
            if user authenticated deals with refresh token

        '''
        try:
            with open(self.path_to_auth, 'r') as f:
                self.authorized_user = json.loads(f.read())

            with open(self.path_to_client, 'r') as fs:
                self.creds = json.loads(fs.read())

            self.gc, self.authorized_user = gspread.oauth_from_dict(
                                                self.creds,
                                                self.authorized_user
                                            )

        except Exception as err:
            print(f'auth failed due to :{err}')
            self.gc = gspread.oauth(
                        credentials_filename = self.path_to_client,
                        authorized_user_filename = self.path_to_auth
               )
        return 1


    def open_google_sheet(self,sheet_id):
        '''
            opens google sheet

        '''
        id_ = sheet_id or self.id
        #print(f'__+__+__+__{id_}_+__+__+__')
        try:
            self.open = self.gc.open_by_key(id_)
        except Exception as err:
            print(f"while Opening google sheet: {err}", type(err))
            if err:
                print("+++++++++ starting fresh authentication ++++++")
            self.explicity_new_auth()


    def fetch_name(self, worksheet, row:int = None, column:int = None, cell:str = None):
        ''' get names Symbol names from sheet '''
        try:
            self.enter_worksheet = self.open.get_worksheet(worksheet)
        except Exception as err:
            print(f"worksheet: {err}")

        """ Prioritze specific cell"""
        if cell:
            try:
                return self.enter_worksheet.acell(cell).value
            except Exception as err:
                print(f"retiving failed: {err}")

        elif row:
            try:
                return self.enter_worksheet.row_values(row)
            except Exception as err:
                print(f"Row retriving failed: {err}")
        else:
            try:
                return self.enter_worksheet.col_values(column)
            except Exception as err:
                print(f"Column retriving failed: {err}")

    def open_worksheet(self,worksheet):
        '''open worksheet to work with'''
        try:
            self.enter_worksheet = self.open.worksheet(worksheet)
        except Exception as err:
            print(f"error opening worksheet : {err}")


    def update_cells(self,cell_number,data):
        ''' update cell with text'''
        try:
            self.enter_worksheet.update_acell(f"{cell_number}", f"{data}")
            self.enter_worksheet.format(f'{cell_number}',{'textFormat': { 'bold': True }, 'backgroundColor': {"red": 0.0, "green": 1.0, "blue": 0.0}, 'verticalAlignment': 'MIDDLE'})
        except Exception as err:
            print(f"error in updating cell with data : {err}")

    def update_img_cells(self, cell_number,data):
        """ update the retrieved data in worksheet """
        try:
            self.enter_worksheet.update_acell(f"{cell_number}", f'=IMAGE("https://raw.githubusercontent.com/lightdrk/stock_Info/main/image_output/{data}",4,900,1000)')
        except Exception as err:
            print(f"updating failed: {err}")

    def worksheet_create(self, name):
        try:
            self.open.add_worksheet(title=name, rows=100,cols=20)
        except Exception as err:
            return 0
        return 1

    def is_worksheet(self,name):
        ''' check for if worksheet avilable 0 yes , 1 no'''
        try:
            self.enter_worksheet = self.open.get_worksheet(name)
        except Exception as err:
            return 1

        return 0

    def test_func(self):
        self.enter_worksheet = self.open.worksheet('TECHNOE')
        self.enter_worksheet.update_acell('B1',"mohit")


"""
def g_sheet(data):
    ''' get data from google sheet using gspread'''
    try:
        with open('authorized_user.json', 'r') as f:
            authorized_user = json.loads(f.read())

        with open('client_secret.json', 'r') as fs:
            creds = json.loads(fs.read())
        #print(authorized_user)
        #print(creds)
        gc, authorized_user = gspread.oauth_from_dict(creds, authorized_user)

    except :

        gc = gspread.oauth(
            credentials_filename = './client_secret.json',
            authorized_user_filename='./authorized_user.json'
        )

    sh = gc.open_by_key('1PKDskq94WwKit6KmVFyop1fZ2yi0eHQoAVYOg7k6JpI')
    worksheet = sh.get_worksheet(0)
    #print(worksheet.acell('A1').value)
    worksheet.update_cell(1,2, 'bingo')
"""

#TODO:cell resizing , add colors to the cell
