import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import MD5 as MD4
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
    kdf = PBKDF2HMAC(
        algorithm=MD4(),
        length=32,
        salt=get_salt(),
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def pad_data(data: bytes) -> bytes:
    block_size = algorithms.AES.block_size // 8
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding


def unpad_data(data: bytes) -> bytes:
    padding_length = data[-1]
    return data[:-padding_length]


def save_encrypted_data(data: str, key: bytes):
    """Шифрует данные в режиме CBC с добавлением случайного IV и сохраняет в файл"""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padded_data = pad_data(data.encode('utf-8'))
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(USERS_FILE, "wb") as f:
        f.write(iv + encrypted_data)


def load_encrypted_data(key: bytes):
    """Загружает и расшифровывает данные, зашифрованные в режиме CBC"""
    with open(USERS_FILE, "rb") as f:
        data = f.read()

    iv = data[:16]
    encrypted_data = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return unpad_data(decrypted_data).decode('utf-8')
