import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

accountSheet = client.open('EncryptBookAccounts').sheet1
postSheet = client.open('EncryptBookPosts').sheet1

def getSalt(username):
    row = accountSheet.col_values(1).index(username)+1
    return accountSheet.cell(row, 3).value.encode('utf-8')

def getKey(username):
    row = accountSheet.col_values(1).index(username)+1
    return accountSheet.cell(row, 4).value.encode('utf-8')

def addAccount(username, passwordHash, salt, key):
    row = int(accountSheet.cell(1,1).value)
    if accountExists(username):
        return False
    accountSheet.update_cell(row, 1, username)
    accountSheet.update_cell(row, 2, passwordHash.decode('utf-8','ignore'))
    accountSheet.update_cell(row, 3, salt.decode('utf-8','ignore'))
    accountSheet.update_cell(row, 4, key.decode('utf-8','ignore'))
    accountSheet.update_cell(1, 1, row+1)

def removeAccount(username):
    if not accountExists(username):
        return False
    row = accountSheet.col_values(1).index(username)+1
    accountSheet.delete_row(row)
    accountSheet.update_cell(1, 1, int(accountSheet.cell(1,1).value)-1)

def accountExists(username):
    column = accountSheet.col_values(1)[1:]
    return username in column

def authenticateAccount(username, passwordHash):
    row = accountSheet.col_values(1).index(username)+1
    goodHash = accountSheet.cell(row, 2).value.encode('utf-8')
    return passwordHash == goodHash
