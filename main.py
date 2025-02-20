import json
import re
import sys
from typing import Optional

import getch
import os

USERS_FILE = "users.json"
ADMIN_USERNAME = "ADMIN"

def mask_input(prompt: Optional[str] = None, mask: str = "*"):
    password = ''
    print(prompt or 'Enter your password: ')
    while True:
        pressedKey = getch.getch()
        if pressedKey == '\n':
            break
        elif pressedKey == "":
            sys.stdout.write("\b")
            sys.stdout.write(" ")
            sys.stdout.write("\b")
            password = password[:-1]
        else:
            password = password + pressedKey
            sys.stdout.write(mask)
    sys.stdout.write("\n")
    return password

def load_users():
    if not os.path.exists(USERS_FILE):
        return {ADMIN_USERNAME: {"password": "", "blocked": False, "password_restricted": False}}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def authenticate():
    users = load_users()
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


def admin_menu(users, username):
    while True:
        print("\nAdmin Menu:")
        print("1. Change admin password")
        print("2. View users")
        print("3. Add user")
        print("4. Block user")
        print("5. Toggle password restriction")
        print("6. About program")
        print("7. Exit")
        print("8. Unblock user(extended)")

        choice = input("Select an option: ")

        if choice == "1":
            change_password(users, username)
        elif choice == "2":
            view_users(users)
        elif choice == "3":
            add_user(users)
        elif choice == "4":
            block_user(users)
        elif choice == "5":
            toggle_restriction(users)
        elif choice == "6":
            print("MuzafarovKR, ИДБ-21-06, var 21")
        elif choice == "7":
            break
        elif choice == "8":
            unblock_user(users)
        else:
            print("Invalid choice.")


def user_menu(users, username):
    while True:
        print("\nUser Menu:")
        print("1. Change password")
        print("2. About program")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            change_password(users, username)
        elif choice == "2":
            print("MuzafarovKR, ИДБ-21-06, var 21")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

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


def main():
    users = load_users()
    username = authenticate()
    if username:
        if username == ADMIN_USERNAME:
            admin_menu(users, username)
        else:
            user_menu(users, username)


if __name__ == "__main__":
    main()
