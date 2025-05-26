import os
import sys
from datetime import datetime
from vault import encrypt_file, decrypt_file, load_key

LOG_FILE = "logs/vault_log.txt"

def log_action(action, filename):
    timestamp = datetime.now()
    with open(LOG_FILE, "a") as log:
        log.write(f"{timestamp} - BatchProcessor - {action}: {filename}\n")

def batch_encrypt(folder_path, key):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            try:
                encrypt_file(full_path, key)
                log_action("Encrypted", filename)
            except Exception as e:
                log_action(f"Encrypt Failed ({e})", filename)

def batch_decrypt(folder_path, key):
    for filename in os.listdir(folder_path):
        if filename.endswith(".enc"):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path):
                try:
                    decrypt_file(full_path, key)
                    log_action("Decrypted", filename)
                except Exception as e:
                    log_action(f"Decrypt Failed ({e})", filename)

def print_usage():
    print("Usage:")
    print("  python batch_processor.py encrypt <folder_path>")
    print("  python batch_processor.py decrypt <folder_path>")

def main():
    if len(sys.argv) != 3:
        print_usage()
        return

    command = sys.argv[1].lower()
    folder_path = sys.argv[2]

    if not os.path.isdir(folder_path):
        print("Error: Provided folder path does not exist.")
        return

    key = load_key()

    if command == "encrypt":
        batch_encrypt(folder_path, key)
        print("Batch encryption completed.")
    elif command == "decrypt":
        batch_decrypt(folder_path, key)
        print("Batch decryption completed.")
    else:
        print("Error: Invalid command.")
        print_usage()

if __name__ == "__main__":
    main()
