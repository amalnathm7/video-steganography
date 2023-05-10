from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

def decrypt_data(ciphertext, key, iv):
    BLOCK_SIZE = 16

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    padded_data = cipher.decrypt(ciphertext)

    data = unpad(padded_data, BLOCK_SIZE)

    return data