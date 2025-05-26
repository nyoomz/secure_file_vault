import os
import getpass
from auth import register_user, login_user
from vault import load_key, encrypt_file, decrypt_file
from datetime import datetime

LOG_FILE = "logs/vault_log.txt"
ENCRYPTED_DIR = "encrypted_files"

def log_action(action, username="System"):
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now()
        log.write(f"{timestamp} - {username} - {action}\n")

def user_menu(username):
    key = load_key()
    while True:
        print(f"\nWelcome, {username}!")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Logout")
    
        choice = input("Select an option: ")

        if choice == "1":
            filepath = input("Enter path to the file to encrypt: ").strip()
            if os.path.isfile(filepath):
                encrypt_file(filepath, key)
                log_action(f"Encrypted file: {filepath}", username)
            else:
                print("File not found.")
        elif choice == "2":
            filename = input("Enter encrypted filename to decrypt: ").strip()
            encrypted_path = os.path.join(ENCRYPTED_DIR, filename)
            if os.path.isfile(encrypted_path):
                decrypt_file(encrypted_path, key)
                log_action(f"Decrypted file: {filename}", username)
            else:
                print("File not found")
        elif choice == "3":
            log_action("Logout", username)
            print("Logged out")
            break
        else:
            print("Invalid option. Please try again")

def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists(ENCRYPTED_DIR):
        os.makedirs(ENCRYPTED_DIR)

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
            if register_user(username, password):
                print("Registration complete")
            else:
                print("Username already exists")
        elif choice == '2':
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
            if login_user(username, password):
                log_action("Login", username)
                user_menu(username)
            else:
                print("Login failed.")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()