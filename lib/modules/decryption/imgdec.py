from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from PIL import Image

key = b'0123456789abcdef' * 2  # 256-bit key
BLOCK_SIZE = 16

image = Image.open('assets/secret_files/images/test.jpg')
width, height = image.size

def encrypt_text(msg):
    # Create an AES cipher object with CBC mode
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Encrypt the message with the cipher object
    ciphertext = cipher.encrypt(pad(msg.encode(), AES.block_size))
    
    # Return the encrypted message and initialization vector (IV)
    return ciphertext, cipher.iv

ciphertext, iv = encrypt_text("Hello world!")

def decrypt_data(ciphertext):
    # Create a new AES cipher object with the key and mode
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Decrypt the ciphertext with the cipher
    padded_data = cipher.decrypt(ciphertext)

    # Unpad the data and return the plaintext
    data = unpad(padded_data, BLOCK_SIZE)

    return data

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
    
    
decrypt_file("assets/secret_files/images/test.jpg.enc",width,height)
    