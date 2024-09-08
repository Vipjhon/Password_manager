from cryptography.fernet import Fernet
import os
import json

# Generate a key for encryption/decryption
def generate_key():
    return Fernet.generate_key()

# Load or create a key
def load_key():
    if os.path.exists("secret.key"):
        return open("secret.key", "rb").read()
    else:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

# Save password to a file
def save_password(account, password):
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())

    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
    else:
        data = {}

    data[account] = encrypted_password.decode()

    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

# Retrieve password from a file
def get_password(account):
    key = load_key()
    cipher_suite = Fernet(key)

    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
        
        encrypted_password = data.get(account)
        if encrypted_password:
            decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
            return decrypted_password.decode()
        else:
            return "Account not found."
    else:
        return "No passwords stored."

# Delete a password from the file
def delete_password(account):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
        
        if account in data:
            del data[account]
            with open("passwords.json", "w") as file:
                json.dump(data, file, indent=4)
            return "Password deleted."
        else:
            return "Account not found."
    else:
        return "No passwords stored."

def main():
    print("Password Manager")
    print("1. Save Password")
    print("2. Get Password")
    print("3. Delete Password")
    print("4. Exit")

    while True:
        choice = input("Choose an option: ")
        
        if choice == "1":
            account = input("Account: ")
            password = input("Password: ")
            save_password(account, password)
            print("Password saved.")
        elif choice == "2":
            account = input("Account: ")
            print("Password:", get_password(account))
        elif choice == "3":
            account = input("Account: ")
            print(delete_password(account))
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
