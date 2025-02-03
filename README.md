# PassStore
PassStore is a project that is created by Parker Sherman to simply, effectively, and convienently store passwords on-device. There can be as many users on one device as each user gets a unique encrypted key! Passwords are also encrypted at the end of every session so there is no need to worry about basic security! There is also a function that allows you to generate a secure password using the secrets python Library.

# HOW TO USE
**Add Password:** Adding a password is simple! Press the Add Password button in the Manage tab and enter a Website and the corresponding password. A password cannot be saved if there is not valid information (Website AND Password)

**Manage Passwords:** Right now the only functionality is to delete passwords, but it the future I plan to add direct editing as well. To delete a password, press Manage Passwords and a list of all current passwords will appear. There is a handy delete button next to each password! To remove the password from the main UI, you must press the "Refresh" button in the main password frame.

**Settings:** There is only one setting and that is to delete your current account. BE CAREFUL!! There is no way to recover an account once deleted, so all information will be lost. In the future, I plan to add color options for the UI here.

**Generate a Password:** In the top right of the main UI there is a frame that allows you to generate a secure password using the secrets library.
This library cryptographically generates a strong, secure password. To generate, drag the slider to your desired length of characters and press generate! The password will appear in the text box for copying or even editing should you choose.
