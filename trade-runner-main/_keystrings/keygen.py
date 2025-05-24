# -*- coding: utf-8 -*-
"""
Created on Mon May  5 07:51:38 2025

@author: seemant
"""

from _common.enc_dec import decrypt
from _common.enc_dec import encrypt


def main():

    """Main function to demonstrate encryption and decryption."""
    pass_key = input("Enter key : ")
    password = input("Enter password: ")

    try:

        encrypted_pass = encrypt(password, pass_key)
        print(f"Encrypted password: {encrypted_pass}")

        #decrypted_pass = decrypt(encrypted_pass, pass_key)
        #print(f"Decrypted password: {decrypted_pass}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()