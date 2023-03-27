import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

key = b'0123456789abcdef' * 2
BLOCK_SIZE = 16
iv = os.urandom(AES.block_size)

def encrypt_image_data(data):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    padded_data = pad(data, BLOCK_SIZE)

    ciphertext = cipher.encrypt(padded_data)

    return ciphertext, key, iv