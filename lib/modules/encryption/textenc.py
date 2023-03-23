from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

# Set the encryption key
key = b'0123456789abcdef' * 2  # 256-bit key

# Define the encryption function for text messages
def encrypt_text(msg):
    # Create an AES cipher object with CBC mode
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Encrypt the message with the cipher object
    ciphertext = cipher.encrypt(pad(msg.encode(), AES.block_size))
    
    # Return the encrypted message and initialization vector (IV)
    return ciphertext, cipher.iv, key

# # Define the decryption function for text messages
# def decrypt_text(ciphertext, iv):
#     # Create an AES cipher object with CBC mode
#     cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
#     # Decrypt the ciphertext with the cipher object
#     plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
#     # Return the decrypted message as a string
#     return plaintext.decode()

# ciphertext, iv = encrypt_text("Hello world!")
# print(iv)
# print(ciphertext)

# # convert bytes to string
# str1 = ciphertext.hex()
# str2 = iv.hex()
# with open("assets/secret_files/texts/test.txt", "w") as file:
#     file.write(str1)
#     file.write('\n')
#     file.write(str2)

# # \xfe,\xe3\x12\xaf\x038\xc8\xad\xb5\xd42\xd2\xa2%n