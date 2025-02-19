"""
Filename: sign_in_ui.py
Author: Parker Sherman
Date: 2025-02-02
Version: 1.0
Description: This is sign in and authentication for PassStore
"""

from customtkinter import *
import customtkinter as ct
import main_screen
import encryption  # Import the encryption module
import time # For making sure the UI doesn't move too fast

def on_sign_in():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        encryption_key = encryption.authenticate_user(username, password)  # Use the authenticate_user function
        if encryption_key:
            root.destroy()  # Close sign-in window
            main_screen.open_main_screen(username)  # Pass encryption key to main screen
        else:
            warning = CTkLabel(frame, text="Invalid Username or Password.", font=("Arial", 14, "bold"), fg_color="#8C2F39", text_color="#E0E0E0", corner_radius=20)
            warning.grid(row=8, column=0, ipadx=5, padx=10, pady=15)
    else:
        warning = CTkLabel(frame, text="Enter a valid Username and Password.", font=("Arial", 14, "bold"), fg_color="#8C2F39", text_color="#E0E0E0", corner_radius=20)
        warning.grid(row=8, column=0, ipadx=5, padx=10, pady=15)

def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")  # Show password
    else:
        password_entry.configure(show="*")  # Hide password

def close_window():
    root.destroy()

# Open the registration window
def open_register_window():
    register_window = CTkToplevel(root)
    register_window.title("Register")
    register_window.geometry("360x300")

    register_window.lift()         # Bring the window to the front
    register_window.focus_force()   # Force focus on the popup
    register_window.grab_set()      # Prevents interacting with the main window until closed

    register_window.grid_columnconfigure(0, weight=1)

    # Register Username and Password Entry
    register_username_entry = CTkEntry(master=register_window, placeholder_text="Username", height=50, width=200, font=("Arial", 18), corner_radius=20)
    register_username_entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    register_password_entry = CTkEntry(master=register_window, show="*", placeholder_text="Password", height=50, width=200, font=("Arial", 18), corner_radius=20)
    register_password_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    # Show Password Checkbox for registration
    show_password_checkbox = CTkCheckBox(register_window, text="Show Password", font=("Arial", 14), command=lambda: toggle_register_password(register_password_entry))
    show_password_checkbox.grid(row=2, column=0, padx=30, pady=(15, 5), sticky="ew")

    # Register Button (handles registration logic)
    def register():
        username = register_username_entry.get()
        password = register_password_entry.get()

        if username and password:
            if encryption.register_user(username, password):
                success = CTkLabel(register_window, text="✅ User Registered!", font=("Arial", 14, "bold"), fg_color="#4CAF50", text_color="#E0E0E0", corner_radius=20)
                success.grid(row=4, column=0, padx=10, pady=15, sticky="ew")
                register_window.update()
                time.sleep(1.5)
                register_window.destroy()
            else:
                CTkLabel(register_window, text="❌ Username already exists!", font=("Arial", 14, "bold"), 
                fg_color="#F44336", text_color="#E0E0E0", corner_radius=20).grid(row=4, column=0, padx=10, pady=15, sticky="ew")

    register_button = CTkButton(register_window, text="Register", font=("Arial", 18, "bold"), command=register, corner_radius=32)
    register_button.grid(row=3, column=0, padx=20, pady=15)

# Toggle show password for registration
def toggle_register_password(password_entry):
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")  # Show password
    else:
        password_entry.configure(show="*")  # Hide password

# Initialize the main window
root = ct.CTk()
root.title("PassStore - Sign In")
root.geometry("360x500")
set_default_color_theme("Oceanix.json")

# Centering the UI components
frame = CTkFrame(master=root, border_width=3)
frame.grid(row=0, column=0, padx=20, pady=20, sticky="enws")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Title Label
title_label = CTkLabel(frame, text="PassStore", font=("Arial", 32, "bold"))
title_label.grid(row=0, column=0, padx=10, pady=(20,10), sticky="ew")

# Username Entry
username_entry = CTkEntry(master=frame, placeholder_text="Username", height=50, width=200, font=("Arial", 18), corner_radius=20)
username_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

# Password Entry
password_entry = CTkEntry(master=frame, show="*", placeholder_text="Password", height=50, width=200, font=("Arial", 18), corner_radius=20)
password_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# Show Password Checkbox
show_password_checkbox = CTkCheckBox(frame, text="Show Password", font=("Arial", 14), command=toggle_password)
show_password_checkbox.grid(row=4, column=0, padx=30, pady=(15, 5), sticky="ew")

# Sign In Button
sign_in_button = CTkButton(frame, text="Sign In", font=("Arial", 18, "bold"), command=on_sign_in, corner_radius=32)
sign_in_button.grid(row=6, column=0, padx=20, pady=15)

# Register Button
register_button = CTkButton(frame, text="Register", font=("Arial", 18, "bold"), command=open_register_window, corner_radius=32)
register_button.grid(row=7, column=0, padx=20, pady=15)

# Center all the elements after they are added
frame.grid_columnconfigure(0, weight=1)

# On pressing the "close application" button, the program will be terminated
root.protocol("WM_DELETE_WINDOW", close_window)

# Prevents resizing of the sign-in window
root.resizable(0,0)

# Run the CTKinter event loop
root.mainloop()
