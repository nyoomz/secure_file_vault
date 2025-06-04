import os
import json
import hashlib
import base64
import secrets
from getpass import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

USER_FILE = "users.json"    #for storing user credentials
SALT_FILE = "salts.json"    #for storing user salts

#save a python dict as a json file
def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

#load a json file and return it as a python dict
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

#register new user, stores hashed pw and random salt
def register_user(username, password):
    users = load_json(USER_FILE)
    salts = load_json(SALT_FILE)

    if username in users:
        print("Username already exists.")
        return

    #hash the pw
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_pw

    #generate and store a random salt per user
    salt = secrets.token_bytes(16)
    salts[username] = base64.b64encode(salt).decode()

    save_json(USER_FILE, users)
    save_json(SALT_FILE, salts)
    print(f"[+] User '{username}' registered.")

#verify user credentials and return a Fernet object for encryption/decryption
def login_user(username, password):
    users = load_json(USER_FILE)
    salts = load_json(SALT_FILE)

    if username not in users:
        print("User not found.")
        return None, None

    #hash the input password and compare with stored hash
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    if users[username] != hashed_pw:
        print("Incorrect password.")
        return None, None

    #derive the Fernet key using the stored salt
    salt = base64.b64decode(salts[username])
    fernet = derive_fernet_key(password, salt)
    print(f"[+] Login successful. Welcome, {username}.")
    return username, fernet

#derive a Fernet key from the password and salt using PBKDF2
#each user has a unique key derived from their password and salt
def derive_fernet_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)