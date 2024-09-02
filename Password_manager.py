from cryptography.fernet import Fernet, InvalidToken
import json
import os

class PasswordManager:
    def __init__(self, master_password, key_file='key.key'):
        self.master_password = master_password
        self.passwords = {}
        self.key_file = key_file
        self.key = self.load_key()
        self.cipher_suite = Fernet(self.key)

    def generate_key(self):
        return Fernet.generate_key()

    def save_key(self):
        with open(self.key_file, 'wb') as key_file:
            key_file.write(self.key)

    def load_key(self):
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, 'rb') as key_file:
                    key = key_file.read()
                    # Validate the key length
                    if len(key) == 44:
                        return key
                    else:
                        print("Invalid key length. Generating a new key.")
            except Exception as e:
                print(f"Error reading key file: {e}")
        # Generate a new key if the existing key is invalid or not found
        self.key = self.generate_key()
        self.save_key()
        return self.key

    def encrypt_password(self, password):
        return self.cipher_suite.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        try:
            return self.cipher_suite.decrypt(encrypted_password.encode()).decode()
        except InvalidToken:
            print("Error: Failed to decrypt password.")
            return None

    def add_password(self, website, username, password):
        encrypted_password = self.encrypt_password(password)
        self.passwords[website] = {'username': username, 'password': encrypted_password}

    def save_passwords(self, filename='passwords.json'):
        with open(filename, 'w') as f:
            json.dump(self.passwords, f, indent=4)

    def load_passwords(self, filename='passwords.json'):
        try:
            with open(filename, 'r') as f:
                self.passwords = json.load(f)
        except FileNotFoundError:
            print("No passwords file found, starting with an empty password manager.")

    def get_password(self, website):
        if website in self.passwords:
            encrypted_password = self.passwords[website]['password']
            decrypted_password = self.decrypt_password(encrypted_password)
            if decrypted_password is not None:
                username = self.passwords[website]['username']
                print(f"Username: {username}, Password: {decrypted_password}")
                return username, decrypted_password
            else:
                print("Error: Failed to retrieve password for", website)
                return None, None
        else:
            print("Error: Website", website, "not found")
            return None, None

if __name__ == "__main__":
    master_password = input("Enter master password: ")
    password_manager = PasswordManager(master_password)

    # Load passwords from file
    password_manager.load_passwords()

    # Add passwords
   # website = input("The web address is: ")
    #username = input("The user name is: ")
   # password = input("The password is: ")
    #password_manager.add_password(website, username, password)

    # Save passwords to file
   # password_manager.save_passwords()

    # Retrieve password for a website
    website = input("Enter the website: ")
    username, password = password_manager.get_password(website)
    if username and password:
        print(f"Username: {username}, Password: {password}")
    else:
        print("Could not retrieve username and password.")