from src.core.functions import load_users, authenticate
from src.core.menu import admin_menu, user_menu

ADMIN_USERNAME = "ADMIN"


def main():
    users = load_users()
    username = authenticate(users)
    if username:
        if username == ADMIN_USERNAME:
            admin_menu(users, username)
        else:
            user_menu(users, username)


if __name__ == "__main__":
    main()
