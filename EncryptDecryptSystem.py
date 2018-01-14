import hashlib
import secrets
import binascii
from Cryptodome.Cipher import AES

def pad(text):
        while len(text) % 8 != 0:
            text += ' '
        return text

def encryptKey(key, keys):
    encryptedKeys = [k for k in keys]
    for i in range(len(keys)):
        aes = AES.new(keys[i], AES.MODE_ECB)
        encryptedKeys[i] = binascii.hexlify(aes.encrypt(key))
    return encryptedKeys

def encryptMessage(message, key):
    aes = AES.new(key, AES.MODE_ECB)
    return binascii.hexlify(aes.encrypt(pad(message).encode('utf-8')))

def hashKeys(keys, salt):
    hashedKeys = [s for s in keys]
    i = 0
    for s in hashedKeys:
        hashedKeys[i] = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', s, salt, 100000))
        i = i+1
    return hashedKeys
