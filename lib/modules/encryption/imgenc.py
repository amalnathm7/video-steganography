from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from PIL import Image

key = b'0123456789abcdef' * 2
BLOCK_SIZE = 16

def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC)

    padded_data = pad(data, BLOCK_SIZE)

    ciphertext = cipher.encrypt(padded_data)

    return ciphertext

def encrypt_img(filename):
    try:
        img = Image.open(filename)
        data = img.tobytes()
    except Exception as e:
        print("Error opening image:", e)
        return
    
    ciphertext = encrypt_data(data)
    output_filename = filename.rsplit('.', 1)[0] + '.enc'
    with open(output_filename, 'wb') as f:
        f.write(ciphertext)
    
    return output_filename