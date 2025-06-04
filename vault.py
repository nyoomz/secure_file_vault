import os
from cryptography.fernet import Fernet
from datetime import datetime

ENCRYPTED_DIR = "encrypted_files"   #directory to store encrypted files
LOG_FILE = "logs/vault_log.txt"     #log file 
os.makedirs(ENCRYPTED_DIR, exist_ok=True)

#encrypt file using fernet obj
def encrypt_file(fernet, filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted_data = fernet.encrypt(data)

    filename = os.path.basename(filepath)
    encrypted_path = os.path.join(ENCRYPTED_DIR, filename + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    print(f"[+] Encrypted → {encrypted_path}")

#decrpy file using provided fernet obj
def decrypt_file(fernet, encrypted_path):
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = fernet.decrypt(encrypted_data)

    filename = os.path.basename(encrypted_path).replace(".enc", "")
    decrypted_path = os.path.join(ENCRYPTED_DIR, "decrypted_" + filename)
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)

    print(f"[+] Decrypted → {decrypted_path}")