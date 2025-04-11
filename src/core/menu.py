import src.core.functions as f

def admin_menu(users, username):
    while True:
        f.clear_screen()
        print("\nМеню (Администратор):")
        print("1. Изменить пароль")
        print("2. Просмотреть пользователей")
        print("3. Добавить пользователя")
        print("4. Заблокировать пользователя")
        print("5. Разблокировать пользователя")
        print("6. Изменить ограничения на пароли")
        print("7. О программе")
        print("8. Выход")

        choice = input("\nВыберите действие: ")

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
            print("Каменский Даниил Викторович, ИДБ-21-07, Вариант 11")
            input("Нажмите Enter, чтобы продолжить...")
        elif choice == "8":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
            input("Нажмите Enter, чтобы продолжить...")


def user_menu(users, username):
    while True:
        f.clear_screen()
        print("\nМеню (Пользователь):")
        print("1. Изменить пароль")
        print("2. О программе")
        print("3. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            f.change_password(users, username)
        elif choice == "2":
            print("Каменский Даниил Викторович, ИДБ-21-07, Вариант 11")
            input("Нажмите Enter, чтобы продолжить...")
        elif choice == "3":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
            input("Нажмите Enter, чтобы продолжить...")
