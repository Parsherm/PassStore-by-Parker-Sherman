"""
Filename: main_screen.py
Author: Parker Sherman
Date: 2025-02-02
Version: 1.0
Description: This is the main bulk of the UI for PassStore
"""

from customtkinter import *
import customtkinter as ct
import PassGenerator
import Manage

# Variable to keep track of the number of passwords
num_of_passwords = 0


# This function makes a frame that displays the current user, and contains a signout button
def user_window(user):
    # Creating the fram that displays the username
    user_frame = CTkFrame(master=window, border_width=3)
    user_frame.grid(row=0, column=0, padx=15, pady=10, sticky="nwes")

    user_frame.grid_columnconfigure(0, weight=1)
    user_frame.grid_rowconfigure(0, weight=1)

    user_label = CTkLabel(user_frame, text="Hello, " + user + "!", font=("Arial", 20, "bold"))
    user_label.grid(row=0, column=0, padx=10, pady=(10,0))
    
    signout = CTkButton(user_frame, text="Signout", command=sign_out)
    signout.grid(row=1, column=0, pady=(10, 20))

# This function closes the application
def sign_out():
    window.destroy()

# This function gets the length of the password based on a slider in pass_gen()
def get_password_length(slider):
    password_length = str(int(slider))
    current_length.configure(text="Password legnth (12-36): " + password_length + " characters")

# This function makes a frame that generates a password for the user
def pass_gen():
    # Creating the password generator
    gen_frame = CTkFrame(window, height=75, border_width=3)
    gen_frame.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

    gen_frame.grid_columnconfigure(0, weight=1)

    # The box where passwords will appear
    global password_entry
    password_entry = CTkEntry(master=gen_frame, placeholder_text="Password", font=("Arial", 14), corner_radius=20)
    password_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    # Show the length of the password as determined by the slider
    global password_length
    password_length = "24"

    global current_length 
    current_length = CTkLabel(gen_frame, text="Password length (12-36): " + password_length + " characters",
                              font=("Arial", 14))
    current_length.grid(row=2, column=1, padx=10, pady=10)

    #This button will refresh the password in the password_entry box
    refresh_btn = CTkButton(gen_frame, text="Generate", command=PassGenerator.generate_password)
    refresh_btn.grid(row=1, column=1, padx=10, pady=5)

    # This slider determines the length olf the password to be generated
    global num_slider
    num_slider = ct.CTkSlider(gen_frame, from_=12, to=36, width=400, number_of_steps=24, height=20, command=get_password_length)
    num_slider.set(24)
    num_slider.grid(row=2, column=0, padx=10, pady=10)

    # Title for the Password Frame
    pass_title = CTkLabel(gen_frame, text="Generate a Password", font=("Arial", 18))
    pass_title.grid(row=0, column=0, padx=(10, 5), pady=5)

# This function makes a frame that allows the user to manage various aspects of the app
def manage_frame():
    

    manage = CTkFrame(window, border_width=3)
    manage.grid(row=1, column=0, padx=15, pady=10, sticky="nwes")

    manage.grid_columnconfigure(0, weight=1)

    frame_title = CTkLabel(manage, text="Manage", font=("Arial", 24))
    frame_title.grid(row=0, column=0, padx=10, pady=10)

    add_btn = CTkButton(manage, text="Add Pasword", font=("Arial", 14), fg_color="transparent", corner_radius=0, border_width=0, 
                        command= Manage.add_password)
    add_btn.grid(row=1, column=0, ipady=5, padx=(3, 3.5), sticky="ew")

    manage_btn = CTkButton(manage, text="Manage Passwords", font=("Arial", 14), fg_color="transparent", corner_radius=0, border_width=0, command= Manage.manage_passwords)
    manage_btn.grid(row=2, column=0, ipady=5, padx=(3, 3.5), sticky="ew")

    settings_btn = CTkButton(manage, text="Settings", font=("Arial", 14), fg_color="transparent", corner_radius=0, border_width=0, command= Manage.open_settings)
    settings_btn.grid(row=3, column=0, ipady=5, padx=(3, 3.5), sticky="ew")

    about_btn = CTkButton(manage, text="About", font=("Arial", 14), fg_color="transparent", corner_radius=0, border_width=0, command= Manage.open_about)
    about_btn.grid(row=4, column=0, ipady=5, padx=(3, 3.5), sticky="ew")

    spacer_box = CTkFrame(manage, border_width=0, height=265, fg_color="#213844")
    spacer_box.grid(row=5, column=0, padx=10, sticky="ew")

    search_bar = CTkEntry(manage, placeholder_text="Search a password")
    search_bar.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

    search_btn = CTkButton(manage, text="Search")
    search_btn.grid(row=7, column=0)

def password_select():

    # Creating the frame that holds the passwords
    global password_frame
    password_frame = CTkScrollableFrame(master=window, label_text="Passwords", border_width=3)
    password_frame.grid(row=1, column=1, padx=20, ipadx=5, pady=10, sticky="nsew")

    password_frame.grid_columnconfigure(0, weight=1)
    password_frame.grid_columnconfigure(1, weight=1)
    password_frame.grid_columnconfigure(2, weight=1)
    password_frame.grid_rowconfigure(0, weight=1)

    user_info = ct.CTkLabel(password_frame, text="Username/Email", font=("Arial", 18))
    user_info.grid(row=0, column=0, pady=(0, 10))

    pass_info = ct.CTkLabel(password_frame, text="Password",  font=("Arial", 18))
    pass_info.grid(row=0, column=1, pady=(0, 10))

    show_password = ct.CTkLabel(password_frame, text="Show",  font=("Arial", 18))
    show_password.grid(row=0, column=2, pady=(0, 10))

    copy_password = ct.CTkLabel(password_frame, text="Copy",  font=("Arial", 18))
    copy_password.grid(row=0, column=3, pady=(0, 10))

def show_password(password_entry):
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")


# Function to add a new password to the scrollable frame
def add_new_password(password_user, password_name):
    global num_of_passwords
    
    # Create a new label with the user name
    stored1_text = ct.CTkEntry(password_frame, height=10, font=("Arial", 14), border_width=0, fg_color="transparent")
    stored1_text.grid(row=num_of_passwords + 1, column=0, pady=5)  # Add it to the scrollable frame
    stored1_text.insert("0", password_user)

    # Add the password
    stored2_text = ct.CTkEntry(password_frame, show="*", font=("Arial", 14), height=10, border_width=0, fg_color="transparent")
    stored2_text.grid(row=num_of_passwords + 1, column=1, pady=5)  # Add it to the scrollable frame
    stored2_text.insert("0", password_name)

    stored1_text.configure(state="disabled")
    stored2_text.configure(state="disabled")

    show_password_checkbox = CTkCheckBox(password_frame, text="", command=lambda: show_password(stored2_text))
    show_password_checkbox.grid(row=num_of_passwords + 1, column=2, padx=10, pady=(10, 5))

    copy_button = ct.CTkButton(password_frame, text="Copy", command=lambda: copy_to_clipboard(stored2_text.get()))
    copy_button.grid(row=num_of_passwords + 1, column=3, padx=10, pady=5)

    num_of_passwords +=1

# This function allows the user to copy a password to the clipboard
def copy_to_clipboard(entry):
    window.clipboard_clear()  # Clear clipboard
    window.clipboard_append(entry)  # Copy entry text
    window.update()  # Keep clipboard data available

def open_main_screen(user, encryption_key):
    global window
    window = ct.CTk()
    window.title("PassStore - Main Dashboard")
    window.geometry("1280x720")

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(1, weight=1)

    set_default_color_theme("Oceanix.json")

    user_window(user)

    pass_gen()

    manage_frame()

    password_select()
    
    window.mainloop() 

     
