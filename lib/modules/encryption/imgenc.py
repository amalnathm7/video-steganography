from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from PIL import Image

import os

# Set the encryption key
key = b'0123456789abcdef' * 2  # 256-bit key

image = Image.open('assets/secret_files/images/test.jpg')
width, height = image.size


# Define the encryption function for text messages
def encrypt_text(msg):
    # Create an AES cipher object with CBC mode
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Encrypt the message with the cipher object
    ciphertext = cipher.encrypt(pad(msg.encode(), AES.block_size))
    
    # Return the encrypted message and initialization vector (IV)
    return ciphertext, cipher.iv

# Define the decryption function for text messages
def decrypt_text(ciphertext, iv):
    # Create an AES cipher object with CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    # Decrypt the ciphertext with the cipher object
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    # Return the decrypted message as a string
    return plaintext.decode()

# Define the encryption function for files (documents, images, videos)


BLOCK_SIZE = 16

def encrypt_data(data):
    # Create a new AES cipher object with the key and mode
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Pad the data to a multiple of the block size
    padded_data = pad(data, BLOCK_SIZE)

    # Encrypt the padded data with the cipher
    ciphertext = cipher.encrypt(padded_data)

    return ciphertext

def encrypt_file(filename):
    # Open the input file and read its contents
    try:
        img = Image.open(filename)
        data = img.tobytes()
        width, height = img.size
    except Exception as e:
        print("Error opening image:", e)
        return
    
    # Encrypt the data with AES and write it to the output file
    ciphertext = encrypt_data(data)
    output_filename = filename + '.enc'
    with open(output_filename, 'wb') as f:
        f.write(ciphertext)
    
    print("Encryption successful! Encrypted file:", output_filename)
    
    return width, height

# Encrypt a text message
ciphertext, iv = encrypt_text("Hello world!")
# print(ciphertext, iv)

# Decrypt the ciphertext
plaintext = decrypt_text(ciphertext, iv)
print(plaintext)


# Encrypt a file
encrypt_file("assets/secret_files/images/test.jpg")

# Decrypt the file
# decrypt_file("assets/secret_files/images/test.jpg.enc",width,height)

# # assets/cover_videos/video.mp4
# # assets/cover_videos/video.mp4.enc

# # assets/secret_files/images/input.jpg
# # assets/secret_files/images/input.jpg.enc

