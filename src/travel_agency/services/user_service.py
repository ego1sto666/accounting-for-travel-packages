"""Бизнес-логика пользователей: регистрация, баланс, управление учетными записями."""

import re

from constants import ROLE_ADMIN, ROLE_CLIENT
from models.user import User
from models.user_role import UserRole
from repositories import booking_repository, user_repository, user_role_repository
from services.auth_service import hash_password

MAX_TOP_UP = 1_000_000


def check_role(user: User, *allowed_roles: int):
    """Проверка прав: действие доступно только перечисленным ролям."""
    if user.user_role not in allowed_roles:
        raise ValueError("Недостаточно прав для этого действия")


def _validate_user_data(login: str, password: str, name: str,
                        surname: str, phone: str | None):
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", login):
        raise ValueError(
            "Логин: от 3 до 20 символов, латинские буквы, цифры и _"
        )
    if len(password) < 6:
        raise ValueError("Пароль должен быть не короче 6 символов")
    if not name.strip():
        raise ValueError("Имя не может быть пустым")
    if not surname.strip():
        raise ValueError("Фамилия не может быть пустой")
    if phone and not re.fullmatch(r"\+?\d{10,15}", phone):
        raise ValueError("Телефон: от 10 до 15 цифр, можно начать с +")


def create_user(login: str, password: str, name: str, surname: str,
                patronymic: str | None, phone: str | None,
                role_id: int) -> int:
    login = login.strip()
    phone = phone.strip() if phone else None
    patronymic = patronymic.strip() if patronymic else None

    _validate_user_data(login, password, name, surname, phone)

    if not user_role_repository.get_by_id(role_id):
        raise ValueError("Такой роли не существует")

    # Сравнение без учета регистра: Ivanov и ivanov считаются одним логином
    for u in user_repository.get_all():
        if u.login.lower() == login.lower():
            raise ValueError("Логин уже занят, выберите другой")

    return user_repository.create(
        login,
        hash_password(password),
        name.strip(),
        surname.strip(),
        patronymic,
        phone,
        role_id,
    )


def register_client(login: str, password: str, name: str, surname: str,
                    patronymic: str | None, phone: str | None) -> int:
    """Самостоятельная регистрация доступна только для роли «Клиент»."""
    return create_user(login, password, name, surname,
                       patronymic, phone, ROLE_CLIENT)


def get_user(user_id: int) -> User:
    user = user_repository.get_by_id(user_id)
    if not user:
        raise ValueError("Пользователь не найден")
    return user


def top_up_balance(user: User, amount: float) -> float:
    check_role(user, ROLE_CLIENT)
    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля")
    if amount > MAX_TOP_UP:
        raise ValueError(f"За один раз можно пополнить не более {MAX_TOP_UP} руб.")

    fresh = get_user(user.user_id)
    new_balance = fresh.balance + amount
    user_repository.update_balance(user.user_id, new_balance)
    return new_balance


# ---------- Функции администратора ----------

def get_roles() -> list[UserRole]:
    return user_role_repository.get_all()


def get_all_users(admin: User) -> list[User]:
    check_role(admin, ROLE_ADMIN)
    return user_repository.get_all()


def add_user(admin: User, login: str, password: str, name: str, surname: str,
             patronymic: str | None, phone: str | None, role_id: int) -> int:
    """Администратор может создать пользователя с любой ролью."""
    check_role(admin, ROLE_ADMIN)
    return create_user(login, password, name, surname,
                       patronymic, phone, role_id)


def change_role(admin: User, user_id: int, role_id: int):
    check_role(admin, ROLE_ADMIN)
    get_user(user_id)
    if user_id == admin.user_id:
        raise ValueError("Нельзя изменить роль самому себе")
    if not user_role_repository.get_by_id(role_id):
        raise ValueError("Такой роли не существует")
    user_repository.update_role(user_id, role_id)


def delete_user(admin: User, user_id: int):
    check_role(admin, ROLE_ADMIN)
    get_user(user_id)
    if user_id == admin.user_id:
        raise ValueError("Нельзя удалить самого себя")
    if booking_repository.count_by_user(user_id) > 0:
        raise ValueError("У пользователя есть брони, удалить его нельзя")
    user_repository.delete(user_id)
