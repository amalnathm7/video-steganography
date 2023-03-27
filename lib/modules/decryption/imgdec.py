from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from PIL import Image

BLOCK_SIZE = 16

def decrypt_data(ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC)

    padded_data = cipher.decrypt(ciphertext)

    data = unpad(padded_data, BLOCK_SIZE)

    return data

def decrypt_file(filename, width, height, key):
    try:
        with open(filename, 'rb') as f:
            ciphertext = f.read()
    except Exception as e:
        print("Error opening file:", e)
        return
    
    plaintext = decrypt_data(ciphertext, key)

    try:
        img = Image.frombytes("RGB", (width, height), plaintext)
        output_filename = filename.rsplit('.', 1)[0] + '.jpg'
        img.save(output_filename)
    except Exception as e:
        print("Error creating PIL image:", e)
        return
    
    return output_filename