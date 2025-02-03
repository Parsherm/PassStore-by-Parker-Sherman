"""
Filename: PassGenerator.py
Author: Parker Sherman
Date: 2025-02-02
Version: 1.0
Description: This program generates the user a secure password once they have clicked the 
    generate button in main_screen.py
"""

import secrets
import string
import main_screen

def generate_password():
    password_length = int(main_screen.num_slider.get())
    main_screen.password_entry.delete(0, "end")

    # Define character sets
    alphabet = string.ascii_letters  # Upper and lower case
    digits = string.digits  # 0-9
    special_chars = string.punctuation  # Special characters

    # Ensure the password contains at least one character from each set
    password_chars = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(digits),
        secrets.choice(special_chars)
    ]

    # Fill the rest with random choices from the full set
    full_set = alphabet + digits + special_chars
    password_chars.extend(secrets.choice(full_set) for _ in range(password_length - 4))

    # Shuffle to remove predictable placement
    secrets.SystemRandom().shuffle(password_chars)

    password = ''.join(password_chars)

    main_screen.password_entry.insert(1, password)

    main_screen.window.update_idletasks()
