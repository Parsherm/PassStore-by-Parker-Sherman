# encryption.py
import json
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import os

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

# Function to authenticate the user
def authenticate_user(username, password):
    """Checks if the username and password are correct, and returns an encryption key if successful."""
    if not os.path.exists(USER_CREDENTIALS_FILE):
        return None  # No users exist yet

    with open(USER_CREDENTIALS_FILE, "r") as file:
        users = json.load(file)

    if username not in users:
        return None  # Username not found

    salt = get_salt(username)
    derived_password = derive_key(password, salt).decode()

    if derived_password == users[username]:
        return derive_key(password, salt)  # Return the encryption key
    else:
        return None  # Incorrect password

# Function to register a new user
def register_user(username, password):
    """Registers a new user by storing a hashed password."""
    if os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, "r") as file:
            users = json.load(file)
    else:
        users = {}

    if username in users:
        print("❌ Username already exists!")
        return False

    salt = get_salt(username)
    hashed_password = derive_key(password, salt).decode()

    users[username] = hashed_password

    with open(USER_CREDENTIALS_FILE, "w") as file:
        json.dump(users, file)

    print("✅ User registered successfully!")
    return True
