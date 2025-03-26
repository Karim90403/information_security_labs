import sys
import tty
import termios
import src.core.functions as f


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def draw_menu(options, current_row, username):
    f.clear_screen()
    print(f"\nПользователь: {username}")
    print("\nМеню:")
    for idx, option in enumerate(options):
        if idx == current_row:
            print(f"> {option}")
        else:
            print(f"  {option}")


def admin_menu(users, username):
    options = [
        "Сменить пароль",
        "Просмотр пользователей",
        "Добавить пользователя",
        "Заблокировать пользователя",
        "Разблокировать пользователя",
        "Изменить ограничения пароля",
        "О программе",
        "Выход"
    ]

    current_row = 0
    draw_menu(options, current_row, username)

    while True:
        key = getch()

        if key == '\x1b':
            key += sys.stdin.read(2)
            if key == '\x1b[A':  # Стрелка вверх
                if current_row > 0:
                    current_row -= 1
            elif key == '\x1b[B':  # Стрелка вниз
                if current_row < len(options) - 1:
                    current_row += 1

        elif key == '\r':
            f.clear_screen()
            if current_row == 0:
                f.change_password(users, username)
            elif current_row == 1:
                f.view_users(users)
            elif current_row == 2:
                f.add_user(users)
            elif current_row == 3:
                f.block_user(users)
            elif current_row == 4:
                f.unblock_user(users)
            elif current_row == 5:
                f.toggle_restriction(users)
            elif current_row == 6:
                print("Дятлова Алина, ИДБ-21-07, Вариант 7")
                input("Нажмите Enter для продолжения...")
            elif current_row == 7:
                break

            draw_menu(options, current_row, username)
            continue

        draw_menu(options, current_row, username)


def user_menu(users, username):
    options = [
        "Сменить пароль",
        "О программе",
        "Выход"
    ]

    current_row = 0
    draw_menu(options, current_row, username)

    while True:
        key = getch()

        if key == '\x1b':
            key += sys.stdin.read(2)

            if key == '\x1b[A' and current_row > 0:
                current_row -= 1
            elif key == '\x1b[B' and current_row < len(options) - 1:
                current_row += 1

        elif key == '\r':
            f.clear_screen()
            if current_row == 0:
                f.change_password(users, username)
            elif current_row == 1:
                print("Дятлова Алина, ИДБ-21-07, Вариант 7")
                input("Нажмите Enter для продолжения...")
            elif current_row == 2:
                break

            draw_menu(options, current_row, username)
            continue

        draw_menu(options, current_row, username)