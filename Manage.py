"""
Filename: Manage.py
Author: Parker Sherman
Date: 2025-02-02
Version: 1.0
Description: This program allows the user to interact with passwords, and also contains an about and settings
"""

import customtkinter as ctk
import main_screen
import encryption
import json

# Function to create a new popup window
def create_popup(title, size="400x300"):
    popup = ctk.CTkToplevel()  # Creates a new window
    popup.geometry(size)
    popup.title(title)

    # Bring the popup to the front and keep it focused
    popup.lift()         # Bring the window to the front
    popup.focus_force()   # Force focus on the popup
    popup.grab_set()      # Prevents interacting with the main window until closed

    return popup  # Return the popup window if further customization is needed

# Function to add a password
def add_password(user):
    popup = create_popup("PassStore - Add Password")

    user_entry = ctk.CTkEntry(popup, width=250, placeholder_text="Enter a Username/Email")
    user_entry.pack(pady=10)
    
    pass_entry = ctk.CTkEntry(popup, width=250, placeholder_text="Enter Password")
    pass_entry.pack(pady=10)

    save_button = ctk.CTkButton(popup, text="Save", command=lambda: save_password(popup, user, user_entry.get(), pass_entry.get()))
    save_button.pack(pady=10)

# Function to manage passwords
def manage_passwords(user):
    popup = create_popup("Manage Passwords")
    popup.title("PassStore - Manage")
    popup.geometry("800x600")

    manage_passwords_frame(popup, user)



# Function to open settings
def open_settings(user):
    popup = create_popup("PassStore - Settings")
    label = ctk.CTkLabel(popup, text="Delete Account?", font=("Arial", 14))
    label.pack(pady=10)

    button = ctk.CTkButton(popup, text="Delete Account?", font=("Arial", 18), command=lambda: delete_account_warning(popup, user))
    button.pack(pady=5)

def delete_account_warning(popup, user):
    warning_label = ctk.CTkLabel(popup, text="Are you sure? \nWARNING: There is no way to \nget an account back after deletion!", font=("Arial", 14))
    warning_label.pack(pady=10)

    delete = ctk.CTkButton(popup, text="Delete", font=("Arial", 18), command=lambda: delete_account(user))
    delete.pack(pady=5)

def delete_account(user_to_delete):
    """Deletes a user and all associated data from the JSON file."""
    try:
        with open("user_credentials.json", "r") as f:
            data = json.load(f)

        # Check if the user exists before attempting to delete
        if user_to_delete in data:
            del data[user_to_delete]  # Remove the user
            with open("user_credentials.json", "w") as f:
                json.dump(data, f, indent=4)  # Save updated JSON
            
            print(f"✅ User '{user_to_delete}' deleted successfully!")
            main_screen.window.destroy()
            return True
        else:
            print(f"❌ User '{user_to_delete}' not found.")
            return False

    except FileNotFoundError:
        print("❌ User credentials file not found.")
        return False

# Function to open the about section
def open_about():
    popup = create_popup("PassStore - About")
    popup.geometry("400x300")
    about = ctk.CTkTextbox(popup, font=("Arial", 14), wrap="word")
    about.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Enable text input temporarily
    about.configure(state="normal")

    # Insert formatted text manually
    about.insert("1.0", "PASSSTORE - ABOUT\n\n")
    about.insert("2.0", "PassStore is a project created by Parker Sherman to securely store passwords on-device.\n\n")

    about.insert("3.0", "HOW TO USE\n",)
    about.insert("4.0", "• ADD PASSWORD: Press the 'Add Password' button in the Manage tab and enter a website & password.\n\n")
    about.insert("5.0", "• MANAGE PASSWORDS: Currently, only deletion is supported, but editing will be added in the future.\n\n")
    about.insert("6.0", "• SETTINGS: You can delete your account, but this action is irreversible!\n\n")
    about.insert("7.0", "• GENERATE A PASSWORD: Use the slider to set the length and generate a secure password using Python’s `secrets` library.\n")

    # Make it read-only again
    about.configure(state="disabled")

# Function to add a password
def save_password(popup, user, name, password):
    if name and password:
        encryption.add_password(user, name, password)

        main_screen.add_new_password(name, password)
        popup.destroy()

def manage_passwords_frame(popup, user):
    passwords_frame =  ctk.CTkScrollableFrame(master=popup, label_text="Passwords", border_width=3)
    passwords_frame.pack(fill="both", expand=True)

    passwords_frame.grid_columnconfigure(0, weight=1)
    passwords_frame.grid_columnconfigure(1, weight=1)
    passwords_frame.grid_columnconfigure(2, weight=1)
    passwords_frame.grid_rowconfigure(0, weight=1)

    user_info = ctk.CTkLabel(passwords_frame, text="Website Name", font=("Arial", 14))
    user_info.grid(row=0, column=0, pady=(0, 10))

    pass_info = ctk.CTkLabel(passwords_frame, text="Password", font=("Arial", 14))
    pass_info.grid(row=0, column=1, pady=(0, 10))

    show_password = ctk.CTkLabel(passwords_frame, text="Show", font=("Arial", 14))
    show_password.grid(row=0, column=2, pady=(0, 10))

    delete_password = ctk.CTkLabel(passwords_frame, text="Delete", font=("Arial", 14))
    delete_password.grid(row=0, column=3, pady=(0, 10))

    passwords = main_screen.get_user_passwords(user)  # Load passwords for this user

    user_data = main_screen.load_user_data(user)
    encryption_key = user_data.get("encryption_key")  # Retrieve user's encryption key

    for idx, password_data in enumerate(passwords):
        encrypted_password = password_data['password'] # Get the encrypted to remove it from the json
        decrypted_password = encryption.decrypt_password(encryption_key, password_data['password'])  # Use imported function
        add_managed_password(passwords_frame, password_data['username'], decrypted_password, encrypted_password, user)  # Display decrypted password

managed_passwords = 0

# Function to add a new password to the scrollable frame
# I would have reused add_new_password() from main_screen.py, but this frame need different functionality (delete button)
def add_managed_password(frame, password_user, password_name, encrypted_password, user):
    global managed_passwords
    
    # Create a new label with the user name
    stored1_text = ctk.CTkEntry(frame, height=10, font=("Arial", 14), border_width=0, fg_color="transparent")
    stored1_text.grid(row=managed_passwords + 1, column=0, pady=5)  # Add it to the scrollable frame
    stored1_text.insert("0", password_user)

    # Add the password
    stored2_text = ctk.CTkEntry(frame, show="*", font=("Arial", 14), height=10, border_width=0, fg_color="transparent")
    stored2_text.grid(row=managed_passwords + 1, column=1, pady=5)  # Add it to the scrollable frame
    stored2_text.insert("0", password_name)

    stored1_text.configure(state="disabled")
    stored2_text.configure(state="disabled")

    show_password_checkbox = ctk.CTkCheckBox(frame, text="", command=lambda: main_screen.show_password(stored2_text))
    show_password_checkbox.grid(row=managed_passwords + 1, column=2, padx=10, pady=(10, 5))

    delete_button = ctk.CTkButton(frame, text="Delete", 
                                  command= lambda: [delete_password(stored1_text.get(), encrypted_password, user),
                                                    remove_password_from_ui(stored1_text, stored2_text, show_password_checkbox, delete_button)])
    delete_button.grid(row=managed_passwords + 1, column=3, padx=10, pady=5)

    managed_passwords += 1

def delete_password(username, password_name, user):
    """Deletes a password entry for a specific username from the user's password list."""
    user_data = encryption.load_user_data()  # Load all user data

    # Get the list of passwords for the user
    password_list = user_data[user]["passwords"]
    print(password_list)
    
    # Check if the password_name exists in the passwords list
    password_to_delete = None
    for entry in password_list:
        if entry["username"] == username and entry["password"] == password_name:
            password_to_delete = entry
            break

    if not password_to_delete:
        print(f"❌ Password for {password_name} not found!")
        return False

    # Remove the found password entry from the list
    user_data[user]["passwords"].remove(password_to_delete)

    # Save updated user data
    encryption.save_user_data(user_data)
    print(f"✅ Password for {password_name} deleted successfully!")


    return True

def remove_password_from_ui(username: ctk.CTkLabel, password: ctk.CTkLabel, show_pass_btn: ctk.CTkLabel, delete_btn: ctk.CTkLabel):
    """Removes the password entry from the UI after deletion from the JSON file."""
    username.destroy()
    password.destroy()
    show_pass_btn.destroy()
    delete_btn.destroy()
    
    
    print(f"✅ Password for {username} deleted from UI!")
