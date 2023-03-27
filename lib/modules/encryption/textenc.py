from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

key = b'0123456789abcdef' * 2

def encrypt_text(msg):
    cipher = AES.new(key, AES.MODE_CBC)
    
    ciphertext = cipher.encrypt(pad(msg.encode(), AES.block_size))
    
    return ciphertext, cipher.iv, key