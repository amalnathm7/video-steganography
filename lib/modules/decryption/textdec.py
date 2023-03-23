from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

def decrypt_text(ciphertext, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return plaintext.decode()

# with open('assets/secret_files/texts/test.txt', 'r') as file:
#     # read contents of file
#     content = file.read()
# ciphertext = bytes.fromhex(content)

# str= []
# # open file in read mode
# with open('assets/secret_files/texts/test.txt', 'r') as file:
#     # read file line by line
#     for line in file:
#         # do something with line
#         str.append(line)

# ciphertext = bytes.fromhex(str[0])
# iv = bytes.fromhex(str[1])
# plaintext = decrypt_text(ciphertext,iv);

# print(plaintext)