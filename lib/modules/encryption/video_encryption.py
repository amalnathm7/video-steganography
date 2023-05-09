import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

# Define the AES encryption/decryption functions
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted_data

def decrypt_data(data, key):
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data

# Define the file encryption/decryption functions
def encrypt_file(filename, key):
    # Open the input file and read the data
    with open(filename, 'rb') as f:
        data = f.read()

    # Encrypt the data using the AES cipher and the key
    encrypted_data = encrypt_data(data, key)

    # Save the encrypted data to a new file with the ".enc" extension
    output_filename = filename + '.enc'
    with open(output_filename, 'wb') as f:
        f.write(encrypted_data)

    print(f'Encrypted file saved as {output_filename}')

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

# Example usage
key = b'0123456789abcdef' * 2  # 256-bit key
encrypt_file('assets/cover_videos/movie.mp4', key)
# decrypt_file('assets/cover_videos/movie.mp4.enc', key)