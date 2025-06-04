
# Secure File Vault in Python

The Secure File Vault is a command-line Python application that allows users to securely encrypt, decrypt, and manage files. It uses modern cryptographic practices to ensure that only authorized users can access sensitive data. This project is a requirement for the course INTECH 3201 – Integrative Programming and Technologies II.


## Demo

Insert gif or link to demo


## Features

- File Encryption and Decryption
    - Encrypts uploaded files using Fernet symmetric encryption
    - Decrypts files on request with the same key
    - Each user has a key 
- User Authentication
    - Register/login with password
    - Passwords are securely hashed using SHA-256
    - Only logged-in users can access the vault features
- Batch Encryption/Decryption Script
    - Separate script batch_processor.py
    - Accepts a folder path and encrypts/decrypts all files inside
- Access Audit Logging
    - All key actions are recorded in logs/vault_log.txt

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nyoomz/secure_file_vault.git
cd secure_file_vault
```

### 2. Setup the Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```


## How to Use

### Run the Main Vault Interface
```python
python main.py
```
- Register or log in using a secure password
- Upload files to encrypt them through filepath
- Decrypt files on demand through filepath
- Actions are logged in logs/vault_log.txt

### Run the Batch Processor
```python
python batch_processor.py <folder_path> <encrypt|decrypt>
```
- Encrypt or decrypt the files in the folder


## Project Structure

```bash
secure_file_vault/
├── main.py               # Main interactive vault app
├── auth.py               # User registration/login logic
├── vault.py              # Encryption/decryption functions
├── batch_processor.py    # CLI batch encrypt/decrypt tool
├── logs/
│   └── vault_log.txt     # Audit trail
├── encrypted_files/      # Storage for encrypted files
├── requirements.txt      # Package dependencies
└── README.md             # Project documentation
```
## Screenshots

### Welcome / Start Screen
![Start](screenshots\start.png)
### User Registration
![Registration](screenshots\register.png)
### Login Process
![Login](screenshots\login.png)
### File Encryption 
![Encryption](screenshots\encrypt_file.png)
![Encryption File](screenshots\encrypt_file_2.png)
### File Decryption 
![Decryption](screenshots\decrypt_file.png)
![Decryption File](screenshots\decrypt_file_2.png)
### File Decryption (Error)
![File Decryption Error](screenshots\decrypt_file_fail_1.png)
![File Decryption Error 2](screenshots\decrypt_file_fail_2.png)
### Batch Processing Encryption
![Batch Processing Enc](screenshots\batch_enc.png)
![Batch Processing Enc 2](screenshots\batch_enc_2.png)
### Batch Processing Decryption
![Batch Processing Enc](screenshots\batch_dec.png)
![Batch Processing Enc 2](screenshots\batch_dec_2.png)
### Audit Log Sample
![App Screenshot](screenshots\logs.png)



