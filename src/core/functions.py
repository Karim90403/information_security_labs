import json
import os
import re
import sys
from json import JSONDecodeError

from src.crypto import generate_key_from_password, save_encrypted_data, load_encrypted_data, USERS_FILE
from src.mask_input import mask_input

ADMIN_USERNAME = "ADMIN"
encrypt_password = None

def clear_screen():
    """Clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def load_users():
    """Loads users from encrypted file"""
    global encrypt_password

    if not os.path.exists(USERS_FILE):
        clear_screen()
        print("File not found. Creating a new encrypted file...")
        initial_data = {ADMIN_USERNAME: {"password": "", "blocked": False, "password_restricted": False}}
        encrypt_password = encrypt_password or mask_input("Enter password to encrypt data: ")
        key = generate_key_from_password(encrypt_password)
        save_encrypted_data(json.dumps(initial_data), key)
        return initial_data

    encrypt_password = encrypt_password or mask_input("Enter password to decrypt data: ")
    key = generate_key_from_password(encrypt_password)
    try:
        return json.loads(load_encrypted_data(key))
    except JSONDecodeError:
        print("Incorrect password.")
        sys.exit(1)


def save_users(users):
    """Saves users to encrypted file"""
    global encrypt_password

    data = json.dumps(users, indent=4)
    encrypt_password = encrypt_password or  mask_input("Enter password to encrypt data: ")
    key = generate_key_from_password(encrypt_password)
    save_encrypted_data(data, key)


def authenticate(users: dict):
    """User authentication"""
    attempts = 3
    while attempts > 0:
        clear_screen()
        print("=== Authentication ===")
        username = input("Enter username: ")

        if username not in users:
            print("User not found. Please try again.")
            input("Press Enter to continue...")
            continue

        user = users[username]

        if user.get("password", "") == "":
            change_password(users, username)
            return username

        password = mask_input("Enter password: ")

        if users[username].get("password_restricted", False) and not validate_password(user.get("password", "")):
            print("Password must contain numbers, arithmetic operators, and numbers again.")
            change_password(users, username)
            return username

        if user.get("blocked"):
            print("Your account is blocked.")
            input("Press Enter to continue...")
            return None

        if user.get("password") == password:
            return username

        print("Incorrect password. Please try again.")
        attempts -= 1
        input("Press Enter to continue...")

    print("Too many failed attempts. Exiting.")
    sys.exit(1)


def validate_password(password):
    """Password complexity validation"""
    return bool(re.match(r"^[0-9]+[+*=%^\/\\-][0-9]+$", password))


def change_password(users, username):
    """User password change"""
    clear_screen()
    print("=== Password Change ===")

    if users[username]["password"] != "":
        old_password = mask_input("Enter old password: ")
        if users[username]["password"] != old_password:
            print("Incorrect password.")
            input("Press Enter to continue...")
            return

    for _ in range(3):
        new_password = mask_input("Enter new password: ")

        if users[username].get("password_restricted", False) and not validate_password(new_password):
            print("Password must contain numbers, punctuation marks, and numbers.")
            continue

        confirm_password = mask_input("Confirm new password: ")

        if new_password != confirm_password:
            print("Passwords don't match.")
            input("Press Enter to continue...")
            return

        users[username]["password"] = new_password
        save_users(users)
        print("Password successfully changed.")
        input("Press Enter to continue...")
        break


def view_users(users):
    """View user list"""
    clear_screen()
    print("=== User List ===")
    for user, data in users.items():
        print(f"User: {user}")
        print(f"  Blocked: {'Yes' if data.get('blocked') else 'No'}")
        print(f"  Password restrictions: {'Yes' if data.get('password_restricted') else 'No'}")
        print("-" * 30)
    input("\nPress Enter to return to menu...")


def add_user(users):
    """Add new user"""
    clear_screen()
    print("=== Add User ===")
    username = input("Enter new username: ")
    if username in users:
        print("User already exists.")
    else:
        users[username] = {"password": "", "blocked": False, "password_restricted": False}
        save_users(users)
        print(f"User {username} successfully added.")
    input("Press Enter to continue...")


def block_user(users):
    """Block user"""
    clear_screen()
    print("=== Block User ===")
    username = input("Enter username to block: ")
    if username in users:
        users[username]["blocked"] = True
        save_users(users)
        print(f"User {username} blocked.")
    else:
        print("User not found.")
    input("Press Enter to continue...")


def unblock_user(users):
    """Unblock user"""
    clear_screen()
    print("=== Unblock User ===")
    username = input("Enter username to unblock: ")
    if username in users:
        users[username]["blocked"] = False
        save_users(users)
        print(f"User {username} unblocked.")
    else:
        print("User not found.")
    input("Press Enter to continue...")


def toggle_restriction(users):
    """Toggle password restrictions"""
    clear_screen()
    print("=== Change Password Restrictions ===")
    username = input("Enter username: ")
    try:
        current = users[username]["password_restricted"]
        users[username]["password_restricted"] = not current
        save_users(users)
        status = "enabled" if not current else "disabled"
        print(f"Password restrictions {status} for user {username}.")
    except KeyError:
        print("User not found.")
    input("Press Enter to continue...")