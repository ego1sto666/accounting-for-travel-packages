"""Вход в систему и регистрация клиента."""

from getpass import getpass

from models.user import User
from services.auth_service import authenticate
from services.user_service import register_client
from ui.common import read_optional, read_text


def login() -> User | None:
    print("\n--- Вход в систему ---")
    login_value = read_text("Логин: ")
    password_value = getpass("Пароль (символы не отображаются): ")

    user = authenticate(login_value, password_value)
    if not user:
        print("Неверный логин или пароль")
        return None

    print(f"Добро пожаловать, {user.name}! Роль: {user.role_name}")
    return user


def register():
    print("\n--- Регистрация клиента ---")
    login_value = read_text("Логин: ")
    password_value = getpass("Пароль (не короче 6 символов): ")
    password_repeat = getpass("Повторите пароль: ")
    if password_value != password_repeat:
        raise ValueError("Пароли не совпадают")

    name = read_text("Имя: ")
    surname = read_text("Фамилия: ")
    patronymic = read_optional("Отчество (можно пропустить): ")
    phone = read_optional("Телефон (можно пропустить): ")

    register_client(login_value, password_value, name, surname,
                    patronymic, phone)
    print("Регистрация прошла успешно! Теперь можно войти.")
