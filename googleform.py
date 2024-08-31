import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
class GoogleForm:
    def __init__(self):

        load_dotenv()
        self.scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
        ]

        self.creds=Credentials.from_service_account_file('credentials.json', scopes=self.scopes)

        self.client=gspread.authorize(self.creds)

        self.sheet_id=os.getenv('SHEET_ID')
        self.sheet=self.client.open_by_key(self.sheet_id)




    def send_values(self,data):
        length_of_data=len(data)
        nested_list=[]
        for e in range(0,length_of_data):
            list=[data[e]["address"],data[e]["price"],data[e]["link"]]
            nested_list.append(list)



        self.sheet.sheet1.append_rows(nested_list)