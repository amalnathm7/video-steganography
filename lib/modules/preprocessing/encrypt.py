from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import os

def encrypt_data(data, isText = False):
    BLOCK_SIZE = 16

    key = b'0123456789abcdef' * 2

    iv = os.urandom(AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    if(isText):
        data = data.encode()
    
    padded_data = pad(data, BLOCK_SIZE)

    ciphertext = cipher.encrypt(padded_data)

    return ciphertext, key, iv