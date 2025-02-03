"""
Filename: Manage.py
Author: Parker Sherman
Date: 2025-02-02
Version: 1.0
Description: This program allows the user to interact with passwords, and also contains an about and settings
"""

import customtkinter as ctk
import main_screen

# Function to create a new popup window
def create_popup(title, size="400x300"):
    popup = ctk.CTkToplevel()  # Creates a new window
    popup.geometry(size)
    popup.title(title)

    # Bring the popup to the front and keep it focused
    popup.lift()         # Bring the window to the front
    popup.focus_force()   # Force focus on the popup
    popup.grab_set()      # Prevents interacting with the main window until closed

    label = ctk.CTkLabel(popup, text=title, font=("Arial", 18))
    label.pack(pady=20)

    return popup  # Return the popup window if further customization is needed

# Function to add a password
def add_password():
    popup = create_popup("Add Password")

    user_entry = ctk.CTkEntry(popup, width=250, placeholder_text="Enter a Username/Email")
    user_entry.pack(pady=10)
    
    pass_entry = ctk.CTkEntry(popup, width=250, placeholder_text="Enter Password")
    pass_entry.pack(pady=10)

    save_button = ctk.CTkButton(popup, text="Save", command=lambda: save_password(popup, user_entry.get(), pass_entry.get()))
    save_button.pack(pady=10)

# Function to manage passwords
def manage_passwords():
    popup = create_popup("Manage Passwords")
    label = ctk.CTkLabel(popup, text="Manage stored passwords here.", font=("Arial", 14))
    label.pack(pady=10)

# Function to open settings
def open_settings():
    popup = create_popup("Settings")
    label = ctk.CTkLabel(popup, text="Modify app settings here.", font=("Arial", 14))
    label.pack(pady=10)

# Function to open the about section
def open_about():
    popup = create_popup("About")
    label = ctk.CTkLabel(popup, text="PassStore \nCreated by Parker Sherman \nDate Created: February 2, 2025", font=("Arial", 14))
    label.pack(pady=10)

# Function to add a password
def save_password(popup, name, password):
    if name and password:
        main_screen.add_new_password(name, password)
        popup.destroy()
