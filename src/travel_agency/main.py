"""Точка входа: проверяет подключение к базе данных и выводит каталог туров."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "database.db"


def main():
    print("Система учета туристических путевок запущена!")

    if not DB_PATH.exists():
        print("База данных не найдена. Сначала выполните: python init_db.py")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    rows = conn.execute(
        "SELECT name, cost, datetimeStart, seats FROM Tour WHERE isAvailable = 1"
    ).fetchall()
    conn.close()

    print("\nДоступные туры:")
    for name, cost, start, seats in rows:
        print(f"  - {name}: {cost:,.0f} руб., начало {start}, мест: {seats}")


if __name__ == "__main__":
    main()
