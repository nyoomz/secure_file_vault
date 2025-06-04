import argparse
import os
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime
from getpass import getpass
import hashlib
import base64

LOG_FILE = "logs/vault_log.txt"

def log_action(action, filename):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} | BATCH_PROCESS | {action.upper()} | {filename}\n")

# derive a key from a password using SHA-256 (demo version)
def load_or_generate_key(password: str):
    hashed_pw = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hashed_pw[:32]))

def encrypt_file(filepath, fernet):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        encrypted_data = fernet.encrypt(data)
        with open(filepath, 'wb') as f:
            f.write(encrypted_data)
        log_action("encrypt", filepath)
    except Exception as e:
        log_action("encrypt_failed", filepath)
        print(f"[ERROR] Could not encrypt {filepath}: {e}")

def decrypt_file(filepath, fernet):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        decrypted_data = fernet.decrypt(data)
        with open(filepath, 'wb') as f:
            f.write(decrypted_data)
        log_action("decrypt", filepath)
    except InvalidToken:
        log_action("decrypt_failed_invalid_token", filepath)
        print(f"[ERROR] Invalid key/token for {filepath}")
    except Exception as e:
        log_action("decrypt_failed", filepath)
        print(f"[ERROR] Could not decrypt {filepath}: {e}")

def process_folder(folder, action, fernet):
    for root, _, files in os.walk(folder):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                if action == "encrypt":
                    encrypt_file(filepath, fernet)
                elif action == "decrypt":
                    decrypt_file(filepath, fernet)

def main():
    # set up the argument parser for command-line usage
    parser = argparse.ArgumentParser(description="Batch encrypt or decrypt files in a folder.")

    # require a folder path and action
    parser.add_argument("folder", help="Folder path to process")
    parser.add_argument("action", choices=["encrypt", "decrypt"], help="Action to perform")

    #parse these arguments into object  
    args = parser.parse_args()

    password = getpass("Enter password for encryption key derivation: ")
    fernet = load_or_generate_key(password)

    #process the folder for enc or dec
    print(f"\n[INFO] Starting batch {args.action}ion for: {args.folder}")
    process_folder(args.folder, args.action, fernet)
    print(f"[INFO] Batch {args.action}ion complete. See {LOG_FILE} for audit logs.\n")

if __name__ == "__main__":
    main()
