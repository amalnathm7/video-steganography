from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

def decrypt_text(ciphertext, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return plaintext.decode()