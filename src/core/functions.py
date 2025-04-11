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
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')


def load_users():
    """Загружает пользователей из зашифрованного файла"""
    global encrypt_password

    if not os.path.exists(USERS_FILE):
        clear_screen()
        print("Файл не найден. Создание нового зашифрованного файла...")
        initial_data = {ADMIN_USERNAME: {"password": "", "blocked": False, "password_restricted": False}}
        encrypt_password = encrypt_password or mask_input("Введите пароль для шифрования данных: ")
        key = generate_key_from_password(encrypt_password)
        save_encrypted_data(json.dumps(initial_data), key)
        return initial_data

    encrypt_password = encrypt_password or mask_input("Введите пароль для расшифровки данных: ")
    key = generate_key_from_password(encrypt_password)
    try:
        return json.loads(load_encrypted_data(key))
    except JSONDecodeError:
        print("Неверный пароль.")
        sys.exit(1)


def save_users(users):
    """Сохраняет пользователей в зашифрованный файл"""
    global encrypt_password

    data = json.dumps(users, indent=4)
    encrypt_password = encrypt_password or  mask_input("Введите пароль для шифрования данных: ")
    key = generate_key_from_password(encrypt_password)
    save_encrypted_data(data, key)


def authenticate(users: dict):
    """Аутентификация пользователя"""
    attempts = 3
    while attempts > 0:
        clear_screen()
        print("=== Аутентификация ===")
        username = input("Введите имя пользователя: ")

        if username not in users:
            print("Пользователь не найден. Пожалуйста, попробуйте снова.")
            input("Нажмите Enter, чтобы продолжить...")
            continue

        user = users[username]

        if user.get("password", "") == "":
            change_password(users, username)
            return username

        password = mask_input("Введите пароль: ")

        if users[username].get("password_restricted", False) and not validate_password(user.get("password", "")):
            print("Пароль должен содержать числа, арифметические операторы и снова числа.")
            change_password(users, username)
            return username

        if user.get("blocked"):
            print("Ваша учетная запись заблокирована.")
            input("Нажмите Enter, чтобы продолжить...")
            return None

        if user.get("password") == password:
            return username

        print("Неверный пароль. Пожалуйста, попробуйте снова.")
        attempts -= 1
        input("Нажмите Enter, чтобы продолжить...")

    print("Слишком много неудачных попыток. Завершение работы.")
    sys.exit(1)


def validate_password(password):
    """Проверка сложности пароля"""
    return bool(re.match(r"^(?=.*[a-zA-Z])(?=.*[А-Яа-яЁё])(?=.*[.,!?;:'\"()\-])[a-zA-ZА-Яа-яЁё.,!?;:'\"()\-]+$/gm", password))


def change_password(users, username):
    """Смена пароля пользователя"""
    clear_screen()
    print("=== Смена пароля ===")

    if users[username]["password"] != "":
        old_password = mask_input("Введите старый пароль: ")
        if users[username]["password"] != old_password:
            print("Неверный пароль.")
            input("Нажмите Enter, чтобы продолжить...")
            return

    for _ in range(3):
        new_password = mask_input("Введите новый пароль: ")

        if users[username].get("password_restricted", False) and not validate_password(new_password):
            print("Пароль должен содержать числа, знаки препинания и снова числа.")
            continue

        confirm_password = mask_input("Подтвердите новый пароль: ")

        if new_password != confirm_password:
            print("Пароли не совпадают.")
            input("Нажмите Enter, чтобы продолжить...")
            return

        users[username]["password"] = new_password
        save_users(users)
        print("Пароль успешно изменен.")
        input("Нажмите Enter, чтобы продолжить...")
        break


def view_users(users):
    """Просмотр списка пользователей"""
    clear_screen()
    print("=== Список пользователей ===")
    for user, data in users.items():
        print(f"Пользователь: {user}")
        print(f"  Заблокирован: {'Да' if data.get('blocked') else 'Нет'}")
        print(f"  Ограничения на пароль: {'Да' if data.get('password_restricted') else 'Нет'}")
        print("-" * 30)
    input("\nНажмите Enter, чтобы вернуться в меню...")


def add_user(users):
    """Добавление нового пользователя"""
    clear_screen()
    print("=== Добавить пользователя ===")
    username = input("Введите имя нового пользователя: ")
    if username in users:
        print("Пользователь уже существует.")
    else:
        users[username] = {"password": "", "blocked": False, "password_restricted": False}
        save_users(users)
        print(f"Пользователь {username} успешно добавлен.")
    input("Нажмите Enter, чтобы продолжить...")


def block_user(users):
    """Блокировка пользователя"""
    clear_screen()
    print("=== Заблокировать пользователя ===")
    username = input("Введите имя пользователя для блокировки: ")
    if username in users:
        users[username]["blocked"] = True
        save_users(users)
        print(f"Пользователь {username} заблокирован.")
    else:
        print("Пользователь не найден.")
    input("Нажмите Enter, чтобы продолжить...")


def unblock_user(users):
    """Разблокировка пользователя"""
    clear_screen()
    print("=== Разблокировать пользователя ===")
    username = input("Введите имя пользователя для разблокировки: ")
    if username in users:
        users[username]["blocked"] = False
        save_users(users)
        print(f"Пользователь {username} разблокирован.")
    else:
        print("Пользователь не найден.")
    input("Нажмите Enter, чтобы продолжить...")


def toggle_restriction(users):
    """Включение/отключение ограничений на пароли"""
    clear_screen()
    print("=== Изменение ограничений на пароли ===")
    username = input("Введите имя пользователя: ")
    try:
        current = users[username]["password_restricted"]
        users[username]["password_restricted"] = not current
        save_users(users)
        status = "включены" if not current else "отключены"
        print(f"Ограничения на пароль {status} для пользователя {username}.")
    except KeyError:
        print("Пользователь не найден.")
    input("Нажмите Enter, чтобы продолжить...")
