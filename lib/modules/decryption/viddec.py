import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

key = b'0123456789abcdef' * 2  # 256-bit key

def decrypt_data(data, key):
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data


def decrypt_file(filename, key):
    # Read the encrypted data from the file
    with open(filename, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt the data using the AES cipher and the key
    decrypted_data = decrypt_data(encrypted_data, key)

    # Save the decrypted data to a new file with the ".dec" extension
    output_filename = filename[:-4] + '.dec' + os.path.splitext(filename)[1]
    with open(output_filename, 'wb') as f:
        f.write(decrypted_data)

    print(f'Decrypted file saved as {output_filename}')
    
decrypt_file('assets/cover_videos/movie.mp4.enc', key)