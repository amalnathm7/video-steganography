from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from PIL import Image
import os

# Set the encryption key
# key = b'0123456789abcdef' * 2  # 256-bit key

def decrypt_text(ciphertext, iv, key):
    # Create an AES cipher object with CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    # Decrypt the ciphertext with the cipher object
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    # Return the decrypted message as a string
    return plaintext.decode()

with open('assets/secret_files/texts/test.txt', 'r') as file:
    # read contents of file
    content = file.read()
ciphertext = bytes.fromhex(content)

str= []
# open file in read mode
with open('assets/secret_files/texts/test.txt', 'r') as file:
    # read file line by line
    for line in file:
        # do something with line
        str.append(line)

ciphertext = bytes.fromhex(str[0])
iv = bytes.fromhex(str[1])
plaintext = decrypt_text(ciphertext,iv);

print(plaintext)