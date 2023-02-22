from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from PIL import Image

import os

# Set the encryption key
key = os.urandom(16)

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

def decrypt_data(ciphertext):
    # Create a new AES cipher object with the key and mode
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Decrypt the ciphertext with the cipher
    padded_data = cipher.decrypt(ciphertext)

    # Unpad the data and return the plaintext
    data = unpad(padded_data, BLOCK_SIZE)

    return data

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

# Define the decryption function for files (documents, images, videos)
def decrypt_file(filename, width, height):
    # Open the input file and read its contents
    try:
        with open(filename, 'rb') as f:
            ciphertext = f.read()
    except Exception as e:
        print("Error opening file:", e)
        return
    
    # Decrypt the data with AES and create a PIL image
    plaintext = decrypt_data(ciphertext)
    try:
        img = Image.frombytes("RGB", (width, height), plaintext)
        output_filename = filename.rsplit('.', 1)[0] + '.jpg'
        img.save(output_filename)
    except Exception as e:
        print("Error creating PIL image:", e)
        return
    
    print("Decryption successful! Decrypted file:", output_filename)

# Encrypt a text message
ciphertext, iv = encrypt_text("Hello, world!")
print(ciphertext, iv)

# Decrypt the ciphertext
plaintext = decrypt_text(ciphertext, iv)
print(plaintext)




# Encrypt a file
encrypt_file("assets/secret_files/images/test.jpg")

# Decrypt the file
decrypt_file("assets/secret_files/images/test.jpg.enc",width,height)

# assets/cover_videos/video.mp4
# assets/cover_videos/video.mp4.enc

# assets/secret_files/images/input.jpg
# assets/secret_files/images/input.jpg.enc

   













































# from Cryptodome.Cipher import AES
# from Cryptodome.Util.Padding import pad

# # Encryption function
# def encrypt(plain_text, key):
#     # Convert the key and plaintext to bytes
#     key = key.encode('utf-8')
#     plain_text = plain_text.encode('utf-8')
    
#     # Create a cipher object and encrypt the plaintext
#     cipher = AES.new(key, AES.MODE_CBC)
#     cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    
#     # Return the initialization vector (IV) and the ciphertext
#     return cipher.iv + cipher_text

# # Example usage
# key = 'mysecretpassword'
# plain_text = 'This is a secret message'
# encrypted_data = encrypt(plain_text, key)

# # Print the encrypted data
# print(encrypted_data)
