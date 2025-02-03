import json
import os
from hashlib import sha256
import secrets

# Path to the user credentials file
CREDENTIALS_FILE = "user_credentials.json"

# Load the existing user data from the JSON file, creating it if it doesn't exist or is empty
def load_user_data():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            # Check if file is empty, if so return an empty dictionary
            data = file.read().strip()
            if data:
                return json.loads(data)
            else:
                return {}
    else:
        # If the file doesn't exist, create it and return an empty dictionary
        save_user_data({})
        return {}

# Save user data to the JSON file
def save_user_data(user_data):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

# Hash the password using SHA-256
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Generate a random encryption key (simply for demonstration purposes)
def generate_encryption_key():
    return secrets.token_hex(16)

# Authenticate the user by checking the username and password
def authenticate_user(username, password):
    user_data = load_user_data()
    hashed_password = hash_password(password)

    if username in user_data and user_data[username]["password"] == hashed_password:
        # Return a simulated encryption key (this could be a more secure key in real use)
        return user_data[username]["encryption_key"]
    return None

# Register a new user
def register_user(username, password):
    user_data = load_user_data()

    if username in user_data:
        return False  # Username already exists

    hashed_password = hash_password(password)
    encryption_key = generate_encryption_key()  # Generate a unique encryption key

    # Store the new user data
    user_data[username] = {
        "password": hashed_password,
        "encryption_key": encryption_key
    }

    save_user_data(user_data)
    return True
