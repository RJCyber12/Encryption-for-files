Homework 3 Encryption Assignemnt
Ryan Fuller
2/19/2024

Discription: 
This program is designed to provide a secure method for encrypting and decrypting files. 
It utilizes AES with a 256 bit key length. 

Features: 
- AES-256
- Secure key management with unique encrytion key and initization vector (IV) so each file
even if identical will contain different encrypted data.


REQUIREMENTS: "cryptography" python library to bypass use of 
OpenSSL header. This library will still use OpenSSL, but will
reduce the need for installation on user machines.
Command to install required packages: pip install cryptography

For use: 

Ensure Python 3.6 or newer is installed.
    Install "cryptography" library with pip:
    Command: pip install cryptography

To encrypt a file:
    Command: python Encryption.py <path_to_input_file> <path_to_encrypted_output_file> encrypt

    NOTES: please keep in mind that you will need to change the path to the paths of your files.
    When you use the encrypt command the encrypted file will be saved
    in the same directory as the input file. 

To decrypt a file:
    Command: python Encryption.py <path_to_encrypted_file> <path_to_decrypted_output_file> decrypt <path_to_key_file>

    NOTES: as before, you will need to change the path. 
    After encrytion a key file is created in the same directory. This file ending in .key should
    be stored in a secure location. If the key is lost, you will be unable to decrypt the encrypted file.
    Additionally, if the key is lost or compromised the file you encrypted is no longer secure. 

Thank you for using my program!

For additonal notes and inquiries please contact: rfuller2@uccs.edu 



