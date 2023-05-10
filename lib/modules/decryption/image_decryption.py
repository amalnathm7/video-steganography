from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

BLOCK_SIZE = 16

def decrypt_image_data(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    padded_data = cipher.decrypt(ciphertext)

    data = unpad(padded_data, BLOCK_SIZE)

    return data