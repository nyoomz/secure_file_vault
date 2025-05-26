import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

ENCRYPTED_DIR = "encrypted_files"

VAULT_KEY = os.getenv("VAULT_KEY")

if not VAULT_KEY:
    raise ValueError("Missing VAULT_KEY in .env file.")

fernet = Fernet(VAULT_KEY.encode())

def encrypt_file(filepath, key):
    with open(filepath, "rb") as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    filename = os.path.basename(filepath)
    encrypted_path = os.path.join(ENCRYPTED_DIR, filename + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    print(f"[+] Encrypted: {filepath} → {encrypted_path}")

def decrypt_file(encrypted_path, key):
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)

    filename = os.path.basename(encrypted_path).replace(".enc", "")
    decrypted_path = os.path.join(os.path.dirname(encrypted_path), "decrypted_" + filename)
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)

    print(f"[+] Decrypted: {encrypted_path} → {decrypted_path}")