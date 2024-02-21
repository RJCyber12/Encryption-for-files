''' 
Homework 3 Encryption Assignemnt
Ryan Fuller
2/19/2024

Discription: 
USE AES-256 in CBC mode to perform encryption and decryption.
Tool can be command line, may develop GUI in the future.
Create random initialization vector for each file and write
to encrypted file and be able to perform decryption function.

REQUIREMENTS: "cryptography" python library to bypass use of 
OpenSSL header. This library will still use OpenSSL, but will
reduce the need for installation on user machines.
Command to install required packages: pip install cryptography


'''

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import sys

'''
Function to generate key and iv values
'''
def generate_key_iv():
    #265bit key
    key = os.urandom(32)
    #128bit IV
    iv = os.urandom(16)
    return key, iv

'''
Function to encrypt file:
will read in file, pad file, and write encrypted data to file.
'''
def encrypt_file(input_file_path, output_file_path, key, iv):
    #encryption algo
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    with open(input_file_path, 'rb') as file_in, open(output_file_path, 'wb') as file_out:
        file_out.write(iv)
        while True:
            chunk = file_in.read(1024)
            if len(chunk) == 0:
                break
            padded_data = padder.update(chunk)
            file_out.write(encryptor.update(padded_data))
        file_out.write(encryptor.update(padder.finalize()) + encryptor.finalize())

def decrypt_file(input_file_path, output_file_path, key):
    with open(input_file_path, 'rb') as f_in:
        iv = f_in.read(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        encrypted_data = f_in.read()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    with open(output_file_path, 'wb') as f_out:
        f_out.write(data)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <input_file> <output_file> [encrypt/decrypt] <key_file (for decryption)>")
        sys.exit(1)
    operation = sys.argv[3]
    if operation == "encrypt":
        key, iv = generate_key_iv()
        encrypt_file(sys.argv[1], sys.argv[2], key, iv)
        # Save the key and IV for later decryption
        with open(sys.argv[2] + ".key", "wb") as key_file:
            key_file.write(key + iv)
        print(f"File encrypted. Key and IV saved to {sys.argv[2]}.key")
    elif operation == "decrypt":
        if len(sys.argv) != 5:
            print("Missing key file for decryption.")
            sys.exit(1)
        with open(sys.argv[4], "rb") as key_file:
            key_iv = key_file.read()
            key = key_iv[:32]
            iv = key_iv[32:]
        decrypt_file(sys.argv[1], sys.argv[2], key)
        print("File decrypted.")
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")


