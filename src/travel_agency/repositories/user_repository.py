"""Работа с таблицей User: CRUD-операции."""

from database.database import get_connection
from models.user import User

# Общая часть запроса: пользователь + название роли из справочника
_SELECT = """
    SELECT u.userID,
           u.login,
           u.password_hash,
           u.name,
           u.surname,
           u.patronymic,
           u.phone,
           u.userRole,
           u.balance,
           r.name
    FROM User u
    JOIN UserRole r ON r.userRoleID = u.userRole
"""


def _map(row) -> User:
    return User(*row)


# ---------- Create ----------

def create(login: str, password_hash: str, name: str, surname: str,
           patronymic: str | None, phone: str | None, role_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO User (login, password_hash, name, surname,
                          patronymic, phone, userRole, balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
    """, (login, password_hash, name, surname, patronymic, phone, role_id))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


# ---------- Read ----------

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE u.userID = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE u.login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY u.userID")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


# ---------- Update ----------

def update_balance(user_id: int, balance: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE User SET balance = ? WHERE userID = ?",
        (balance, user_id),
    )
    conn.commit()
    conn.close()


def update_role(user_id: int, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE User SET userRole = ? WHERE userID = ?",
        (role_id, user_id),
    )
    conn.commit()
    conn.close()


# ---------- Delete ----------

def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM User WHERE userID = ?", (user_id,))
    conn.commit()
    conn.close()
