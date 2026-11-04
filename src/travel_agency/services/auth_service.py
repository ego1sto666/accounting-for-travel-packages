"""Авторизация: хеширование пароля и проверка логина/пароля."""

import hashlib

from models.user import User
from repositories import user_repository


def hash_password(password: str) -> str:
    """В базе хранится не пароль, а его хеш SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str) -> User | None:
    user = user_repository.get_by_login(login.strip())
    if not user:
        return None
    if user.password_hash != hash_password(password):
        return None
    return user
