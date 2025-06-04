import os
import getpass
from auth import register_user, login_user
from vault import encrypt_file, decrypt_file
from datetime import datetime

LOG_FILE = "logs/vault_log.txt"
ENCRYPTED_DIR = "encrypted_files"

def log_action(action, username="System"):
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now()
        log.write(f"{timestamp} - {username} - {action}\n")

def intro_border(text):
    print ("\n")
    print("=" * 50)
    print("|{:^48}|".format(""))
    print("|{:^48}|".format(text))
    print("|{:^48}|".format(""))
    print("=" * 50)

def user_menu(username, fernet):
    while True:
        intro_border("  MENU   ")
        print(f"\nWelcome, {username}!")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Logout")
    
        choice = input("\nChoose an option: ")

        if choice == "1":
            intro_border(" ENCRYPT FILE ")
            filename = input("Enter path to the file to encrypt: ").strip()
            filepath = filename
            if os.path.isfile(filepath):
                encrypt_file(fernet, filepath)
                log_action(f"Encrypted file: {filename}", username)
            else:
                print("File not found.")
        elif choice == "2":
            intro_border(" DECRYPT FILE ")
            filename = input("Enter encrypted filename to decrypt: ").strip()
            filepath = os.path.join(ENCRYPTED_DIR, filename)
            if os.path.isfile(filepath):
                decrypt_file(fernet, filepath)
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
        intro_border(" SECURE FILE VAULT ")    
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            intro_border(" REGISTRATION ")
            username = input("\nEnter username: ").strip()
            password = getpass.getpass("Enter password: ")
            register_user(username, password)
            log_action("Registration", username)
        elif choice == '2':
            intro_border(" LOGIN ")
            username = input("\nEnter username: ").strip()
            password = getpass.getpass("Enter password: ")
            fernet = login_user(username, password)
            log_action("Login", username)
            user_menu(username, fernet)
        elif choice == "3":
            print("Thank you ! Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()