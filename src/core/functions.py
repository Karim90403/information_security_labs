import json
import os
import re

from src.crypto import generate_key_from_password, save_encrypted_data, load_encrypted_data, USERS_FILE
from src.mask_input import mask_input

ADMIN_USERNAME = "ADMIN"

def load_users():
    if not os.path.exists(USERS_FILE):
        print("File not found. Creating a new encrypted file...")
        # Создаем новый файл с минимальными данными
        initial_data = {ADMIN_USERNAME: {"password": "", "blocked": False, "password_restricted": False}}
        password = input("Enter password to encrypt the new file: ")
        key = generate_key_from_password(password)
        save_encrypted_data(json.dumps(initial_data), key)
        return initial_data  # Возвращаем начальные данные
    password = input("Enter password to decrypt data: ")
    key = generate_key_from_password(password)
    return json.loads(load_encrypted_data(key))

def save_users(users):
    data = json.dumps(users, indent=4)
    password = input("Enter password to encrypt data: ")
    key = generate_key_from_password(password)
    save_encrypted_data(data, key)

def authenticate(users: dict):
    attempts = 3
    while attempts > 0:
        username = input("Enter username: ")

        if username not in users:
            print("User not found. Try again.")
            continue

        user = users[username]

        if user.get("password", "") == "":
            change_password(users, username)
            return

        password = mask_input("Enter password: ")

        if users[username].get("password_restricted", False) and not validate_password(user.get("password", "")):
            print("Password must alternate letters, punctuation, and letters.")
            change_password(users, username)
            return

        if user.get("blocked"):
            print("Your account is blocked.")
            return

        if user.get("password") == password:
            return username

        print("Incorrect password. Try again.")
        attempts -= 1

    print("Too many failed attempts. Exiting.")
    return

def validate_password(password):
    return bool(re.match(r"^[A-Za-z]+[!@#$%^&*(),.?\":{}|<>][A-Za-z]+$", password))

def change_password(users, username):
    old_password = mask_input("Enter old password: ")
    try:
        if users[username]["password"] != old_password:
            print("Incorrect password.")
            return
        for _ in range(3):
            new_password = mask_input("Enter new password: ")

            if users[username].get("password_restricted", False) and not validate_password(new_password):
                print("Password must alternate letters, punctuation, and letters.")
                continue

            confirm_password = mask_input("Confirm new password: ")

            if new_password != confirm_password:
                print("Passwords do not match.")
                return

            users[username]["password"] = new_password
            save_users(users)
            print("Password changed successfully.")
            break
    except KeyError:
        print("User not found.")


def view_users(users):
    for user, data in users.items():
        print(f"User: {user}, Blocked: {data.get('blocked')}, Restriction: {data.get('password_restricted')}")


def add_user(users):
    username = input("Enter new username: ")
    if username in users:
        print("User already exists.")
        return
    save_users(users)
    users[username] = {"password": "", "blocked": False, "password_restricted": False}
    print("User added.")


def block_user(users):
    username = input("Enter username to block: ")
    if username in users:
        users[username]["blocked"] = True
        save_users(users)
        print("User blocked.")
    else:
        print("User not found.")

def unblock_user(users):
    username = input("Enter username to un block: ")
    if username in users:
        users[username]["blocked"] = False
        save_users(users)
        print("User unblocked.")
    else:
        print("User not found.")

def toggle_restriction(users):
    username = input("Enter username to toggle restriction: ")
    try:
        users[username]["password_restricted"] = not users[username]["password_restricted"]
        save_users(users)
        print("Restriction toggled.")
    except KeyError:
        print("User not found.")