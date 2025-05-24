# -*- coding: utf-8 -*-
"""
Created on Mon May  5 07:51:38 2025

@author: seemant
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def derive_key(pass_key: str) -> bytes:
    # Use SHA256 to derive a key from the pass_key
    salt = b'salt_'  # Fixed salt for simplicity; in production, use random salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_key.encode()))
    return key


def encode_no_colon(data: bytes) -> str:
    # Encode bytes to base64 with custom alphabet to avoid colons
    encoded = base64.b64encode(data, altchars=b'-_').decode('utf-8')
    return encoded


def decode_no_colon(encoded: str) -> bytes:
    # Decode base64 with custom alphabet
    return base64.b64decode(encoded.encode('utf-8'), altchars=b'-_')


def encrypt(text: str, pass_key: str) -> str:
    # Derive key from pass_key using SHA256
    key = derive_key(pass_key)
    fernet = Fernet(key)
    
    # Encrypt the text
    encrypted = fernet.encrypt(text.encode('utf-8'))
    
    # Encode to avoid colons
    return encode_no_colon(encrypted)


def decrypt(encrypted_text: str, pass_key: str) -> str:
    if pass_key is None:
        return encrypted_text
    try:
        # Derive key from pass_key using SHA256
        key = derive_key(pass_key)
        fernet = Fernet(key)
        
        # Decode the custom base64
        encrypted_bytes = decode_no_colon(encrypted_text)
        
        # Decrypt
        decrypted = fernet.decrypt(encrypted_bytes).decode('utf-8')
        return decrypted
    except Exception as e:
        return f"Decryption error: {str(e)}"

if __name__ == "__main__":
    password = "Hello World!"
    pass_key = "secret"
    
    encrypted_pass = encrypt(password, pass_key)
    print(f"Encrypted password: {encrypted_pass}")

    decrypted_pass = decrypt(encrypted_pass, pass_key)
    print(f"Decrypted password: {decrypted_pass}")
