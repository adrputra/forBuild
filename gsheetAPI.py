# For get storage.json
# from gsheets import Sheets
# sheets = Sheets.from_files('~/client_secrets.json', '~/storage.json')

import gspread
from google.oauth2.service_account import Credentials

def getDataSheetInstagram():
    gc = gspread.oauth(
        credentials_filename='client_secrest.json',
        authorized_user_filename='storage.json'
    )

    sh = gc.open_by_key('18k_NEd0jVj6x0gBcF0dAM3CF9O-lKJES5J5DJLbSZ5E')

    result = sh.sheet1.col_values(3)

    IgID = []

    for i in range(1,len(result)):
        IgID.append(result[i].split('reel')[1].split('/')[1])
    print(IgID)
    return IgID

# getDataSheet()
