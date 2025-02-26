import src.core.functions as f

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
            f.change_password(users, username)
        elif choice == "2":
            f.view_users(users)
        elif choice == "3":
            f.add_user(users)
        elif choice == "4":
            f.block_user(users)
        elif choice == "5":
            f.toggle_restriction(users)
        elif choice == "6":
            print("MuzafarovKR, ИДБ-21-06, var 21")
        elif choice == "7":
            break
        elif choice == "8":
            f.unblock_user(users)
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
            f.change_password(users, username)
        elif choice == "2":
            print("MuzafarovKR, ИДБ-21-06, var 21")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
