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
#packages
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import sys

'''
Function to generate key and iv values.
Returns:
    - key (bytes): The generated 256-bit encryption key.
    - iv (bytes): The generated 128-bit initialization vector.
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
Parameters:
    - input_file_path (str): Path to the input file to be encrypted.
    - output_file_path (str): Path where the encrypted file will be saved.
    - key (bytes): The encryption key, 256 bits in length.
    - iv (bytes): The initialization vector, 128 bits in length.

    This function reads the input file, applies PKCS7 padding, encrypts the data,
    and writes the IV followed by the encrypted data to the output file.
'''
def encrypt_file(input_file_path, output_file_path, key, iv):
    #encryption algo setup
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

'''
Decrypts a file encrypted by the encrypt_file function.

    Parameters:
    - input_file_path (str): Path to the encrypted file to be decrypted.
    - output_file_path (str): Path where the decrypted file will be saved.
    - key (bytes): The encryption key used during encryption, 256 bits in length.

    Reads the IV from the start of the encrypted file, then decrypts the remaining data
    and removes the PKCS7 padding before writing the original data to the output file.
'''
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
    #command line usage
    if len(sys.argv) < 4:
        print("Usage: python script.py <input_file> <output_file> [encrypt/decrypt] <key_file (for decryption)>")
        sys.exit(1)
    operation = sys.argv[3]
    if operation == "encrypt":
        #gem the key and iv
        key, iv = generate_key_iv()
        #encrypt file
        encrypt_file(sys.argv[1], sys.argv[2], key, iv)
        #save the key and IV for later decryption
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


