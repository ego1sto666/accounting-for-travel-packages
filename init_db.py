"""Создание базы данных database.db из файла schema.sql."""

import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DB_PATH = PROJECT_DIR / "database.db"
SCHEMA_PATH = PROJECT_DIR / "schema.sql"


def init_database():
    if not SCHEMA_PATH.exists():
        print(f"Ошибка: файл {SCHEMA_PATH.name} не найден в корне проекта!")
        return

    sql_script = SCHEMA_PATH.read_text(encoding="utf-8")

    conn = sqlite3.connect(DB_PATH)
    print(f"Подключение к базе данных: {DB_PATH.name}")
    conn.executescript(sql_script)
    conn.commit()
    conn.close()

    print("База данных создана и заполнена тестовыми данными из schema.sql")


if __name__ == "__main__":
    init_database()
