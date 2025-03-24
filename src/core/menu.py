import src.core.functions as f

def admin_menu(users, username):
    while True:
        f.clear_screen()
        print("\nМеню(админимстратор):")
        print("1. Сменить пароль")
        print("2. Просмотр пользователей")
        print("3. Добавить пользователя")
        print("4. Заблокировать пользователя")
        print("5. Разблокировать пользователя")
        print("6. Изменить ограничения пароля")
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
            print("Салий Захар, ИДБ-21-07, Варинат 25")
            input("Нажмите Enter для продолжения...")
        elif choice == "8":
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")
            input("Нажмите Enter для продолжения...")


def user_menu(users, username):
    while True:
        f.clear_screen()
        print("\nМеню(пользователь):")
        print("1. Сиенить пароль")
        print("2. О нас")
        print("3. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            f.change_password(users, username)
        elif choice == "2":
            print("Салий Захар, ИДБ-21-07, Варинат 25")
            input("Нажмите Enter для продолжения...")
        elif choice == "3":
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")
            input("Нажмите Enter для продолжения...")
