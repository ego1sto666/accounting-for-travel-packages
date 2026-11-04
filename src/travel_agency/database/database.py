"""Подключение к базе данных SQLite."""

import sqlite3
from pathlib import Path

# database.db лежит в корне проекта: src/travel_agency/database/ -> корень
DB_PATH = Path(__file__).resolve().parents[3] / "database.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    # В SQLite проверка внешних ключей по умолчанию выключена
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def database_exists() -> bool:
    return DB_PATH.exists()
