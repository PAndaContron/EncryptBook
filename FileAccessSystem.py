import gspread
from oauth2client.service_account import ServiceAccountCredentials
import binascii

import EncryptDecryptSystem as cryptSystem

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

accountSheet = client.open('EncryptBookAccounts').sheet1
postSheet = client.open('EncryptBookPosts').sheet1

def getSalt(username):
    row = accountSheet.col_values(1).index(username)+1
    return binascii.unhexlify(accountSheet.cell(row, 3).value.encode('utf-8'))

def getKey(username):
    row = accountSheet.col_values(1).index(username)+1
    return binascii.unhexlify(accountSheet.cell(row, 4).value.encode('utf-8'))

def addAccount(username, passwordHash, salt, key):
    row = int(accountSheet.cell(1,1).value)
    if accountExists(username):
        return False
    accountSheet.update_cell(row, 1, username)
    accountSheet.update_cell(row, 2, passwordHash.decode('utf-8','ignore'))
    accountSheet.update_cell(row, 3, binascii.hexlify(salt).decode('utf-8','ignore'))
    accountSheet.update_cell(row, 4, binascii.hexlify(key).decode('utf-8','ignore'))
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

def authenticateAccount(username, password):
    row = accountSheet.col_values(1).index(username)+1
    passwordHash = cryptSystem.shaHash(password.encode('utf-8'), getSalt(username))
    goodHash = accountSheet.cell(row, 2).value.encode('utf-8')
    return passwordHash == goodHash

def createAccount(username, password):
    salt = cryptSystem.generate(16)
    passwordHash = cryptSystem.shaHash(password.encode('utf-8'), salt)
    key = cryptSystem.generate(16)
    addAccount(username, passwordHash, salt, key)

def addGroupKey(username, groupKey):
    row = accountSheet.col_values(1).index(username)+1
    for i in range(len(accountSheet.row_values(row))):
        print('')

def createPost(content, keys, username):
    salt = cryptSystem.generate(16)
    key = cryptSystem.generate(16)
    encKeys = cryptSystem.encryptKey(key, keys)
    hashKeys = cryptSystem.hashKeys(keys, salt)
    encMessage = cryptSystem.encryptMessage(content, key)
    row = int(postSheet.cell(1,1).value)
    postSheet.update_cell(row, 1, username)
    postSheet.update_cell(row, 2, binascii.hexlify(salt).decode('utf-8','ignore'))
    postSheet.update_cell(row, 3, encMessage.decode('utf-8','ignore'))
    postSheet.update_cell(row, 4, len(keys))
    for i in range(len(keys)):
        index1 = 5+(i*2)
        index2 = index1+1
        postSheet.update_cell(row, index1, binascii.hexlify(encKeys[i]).decode('utf-8','ignore'))
        postSheet.update_cell(row, index2, binascii.hexlify(hashKeys[i]).decode('utf-8','ignore'))
    postSheet.update_cell(1, 1, row+1)

def readPost(row, username):
    myKey = getKey(username)
    salt = binascii.unhexlify(postSheet.cell(row, 2).value.encode('utf-8'))
    hashKey = cryptSystem.shaHash(myKey, salt)
    keyIndex = 0
    for i in range(len(postSheet.row_values(row))):
        if i>4 and i%2==0 and binascii.unhexlify(postSheet.cell(row, i).value.encode('utf-8'))==hashKey:
            keyIndex = i-1
            break
    encKey = postSheet.cell(row, keyIndex).value.encode('utf-8')
    print(encKey)
    key = cryptSystem.decrypt(encKey, myKey)
    print(key)
    encText = binascii.hexlify(postSheet.cell(row, 3).value.encode('utf-8'))
    print(encText)
    return binascii.hexlify(cryptSystem.decrypt(encText, key)).decode('utf-8', 'ignore')
    
