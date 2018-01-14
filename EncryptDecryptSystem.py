import hashlib
import os
import binascii
from Cryptodome.Cipher import AES

def pad(text):
    while len(text) % 16 != 0:
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

def decrypt(text, key):
    aes = AES.new(key, AES.MODE_ECB)
    text = binascii.unhexlify(text)
    return aes.decrypt(text)

def hashKeys(keys, salt):
    hashedKeys = [s for s in keys]
    i = 0
    for s in hashedKeys:
        hashedKeys[i] = shaHash(s, salt)
        i = i+1
    return hashedKeys

def shaHash(text, salt):
    return binascii.hexlify(hashlib.pbkdf2_hmac('sha256', text, salt, 100000))

def generate(length):
    return os.urandom(length))
