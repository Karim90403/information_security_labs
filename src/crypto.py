import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

USERS_FILE = "users.txt"
SALT_FILE = "salt.bin"

def get_salt():
    """Загружает SALT из файла или генерирует новый, если его нет."""
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def generate_key_from_password(password: str):
    kdf = PBKDF2HMAC(algorithm=hashes.MD5(), length=32, salt=get_salt(), iterations=100000, backend=default_backend())
    return kdf.derive(password.encode())


def save_encrypted_data(data: str, key: bytes):
    iv = os.urandom(16)  # Инициализационный вектор
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    # Сохраняем IV + зашифрованные данные
    with open(USERS_FILE, "wb+") as f:
        f.write(iv + encrypted_data)


def load_encrypted_data(key: bytes):
    with open(USERS_FILE, "rb+") as f:
        encrypted_data = f.read()

    iv = encrypted_data[:16]  # Первые 16 байтов — это IV
    encrypted_data = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode("latin-1")
