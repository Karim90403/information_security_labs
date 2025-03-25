import src.core.functions as f

def admin_menu(users, username):
    while True:
        f.clear_screen()
        print("\nMenu (Administrator):")
        print("1. Change password")
        print("2. View users")
        print("3. Add user")
        print("4. Block user")
        print("5. Unblock user")
        print("6. Change password restrictions")
        print("7. About")
        print("8. Exit")

        choice = input("\nSelect an action: ")

        if choice == "1":
            f.change_password(users, username)
        elif choice == "2":
            f.view_users(users)
        elif choice == "3":
            f.add_user(users)
        elif choice == "4":
            f.block_user(users)
        elif choice == "5":
            f.unblock_user(users)
        elif choice == "6":
            f.toggle_restriction(users)
        elif choice == "7":
            print("Zakhar Saliy, IDB-21-07, Variant 25")
            input("Press Enter to continue...")
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")


def user_menu(users, username):
    while True:
        f.clear_screen()
        print("\nMenu (User):")
        print("1. Change password")
        print("2. About")
        print("3. Exit")

        choice = input("\nSelect an action: ")

        if choice == "1":
            f.change_password(users, username)
        elif choice == "2":
            print("Zakhar Saliy, IDB-21-07, Variant 25")
            input("Press Enter to continue...")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")