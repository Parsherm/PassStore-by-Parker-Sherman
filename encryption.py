"""
Filename: encryption.py
Author: Parker Sherman
Date: 2025-02-02
Version: 1.0
Description: This program encrypts all the user's data
"""
import json
import base64
import hashlib
import os
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding



# 📂 File to store user credentials (hashed passwords)
USER_CREDENTIALS_FILE = "user_credentials.json"

# Function to get a salt from the username
def get_salt(username):
    return hashlib.sha256(username.encode()).digest()  # 32-byte salt

# Function to derive an encryption key from the password
def derive_key(password, salt):
    """Derives the encryption key from the password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Function to hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to generate a random encryption key
def generate_encryption_key():
    return secrets.token_hex(16)  # 16 bytes = 32 hex characters

# Function to load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, "r") as file:
            data = file.read().strip()
            if data:
                return json.loads(data)
            else:
                return {}
    else:
        save_user_data({})
        return {}

# Function to save user data to the JSON file
def save_user_data(user_data):
    with open(USER_CREDENTIALS_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

# Function to register a new user
def register_user(username, password):
    """Registers a new user by storing a hashed password and an empty list for passwords."""
    user_data = load_user_data()

    if username in user_data:
        print("❌ Username already exists!")
        return False

    salt = get_salt(username)
    hashed_password = derive_key(password, salt).decode()
    encryption_key = generate_encryption_key()

    # Store the new user data
    user_data[username] = {
        "hashed_password": hashed_password,
        "encryption_key": encryption_key,
        "passwords": []  # Initially empty list for passwords
    }

    save_user_data(user_data)
    print("✅ User registered successfully!")
    return True

# Function to authenticate a user
def authenticate_user(username, password):
    """Authenticates a user by checking the username and password."""
    user_data = load_user_data()

    if username not in user_data:
        print("❌ Username not found!")
        return None

    salt = get_salt(username)
    derived_password = derive_key(password, salt).decode()

    if derived_password == user_data[username]["hashed_password"]:
        print("✅ Authentication successful!")
        return user_data[username]["encryption_key"]
    else:
        print("❌ Incorrect password!")
        return None

def add_password(username, password_username, new_password):
    """Encrypts and stores a new password with an associated username."""
    user_data = load_user_data()

    if username not in user_data:
        print("❌ Username not found!")
        return False

    encryption_key = user_data[username]["encryption_key"]
    encrypted_password = encrypt_password(encryption_key, new_password)

    password_entry = {
        "username": password_username,
        "password": encrypted_password
    }
    user_data[username]["passwords"].append(password_entry)
    save_user_data(user_data)
    print("✅ Password added successfully (Encrypted)!")
    return True



def view_passwords(username):
    """Returns the decrypted list of passwords for a user."""
    user_data = load_user_data()

    if username not in user_data:
        print("❌ Username not found!")
        return None

    encryption_key = user_data[username]["encryption_key"]
    decrypted_passwords = []

    for entry in user_data[username]["passwords"]:
        decrypted_passwords.append({
            "username": entry["username"],
            "password": decrypt_password(encryption_key, entry["password"])
        })

    return decrypted_passwords



def encrypt_password(encryption_key, password):
    """Encrypts a password using AES with PKCS7 padding."""
    key = base64.urlsafe_b64decode(encryption_key)  # Decode key from base64
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Apply PKCS7 padding to match AES block size (16 bytes)
    padder = padding.PKCS7(128).padder()
    padded_password = padder.update(password.encode()) + padder.finalize()

    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()

    # Store IV + encrypted password (Base64-encoded)
    return base64.b64encode(iv + encrypted_password).decode()


def decrypt_password(encryption_key, encrypted_password):
    """Decrypts an AES-encrypted password using PKCS7 unpadding."""
    key = base64.urlsafe_b64decode(encryption_key)
    encrypted_data = base64.b64decode(encrypted_password)

    iv = encrypted_data[:16]  # Extract IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    decrypted_padded_password = decryptor.update(encrypted_data[16:]) + decryptor.finalize()

    # Remove PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_password = unpadder.update(decrypted_padded_password) + unpadder.finalize()

    return decrypted_password.decode()

