"""Работа с таблицей Tour: CRUD-операции."""

from database.database import get_connection
from models.tour import Tour

_SELECT = """
    SELECT tourID,
           name,
           cost,
           datetimeStart,
           datetimeEnd,
           seats,
           isAvailable,
           description
    FROM Tour
"""


def _map(row) -> Tour:
    return Tour(*row)


# ---------- Create ----------

def create(name: str, cost: float, datetime_start: str, datetime_end: str,
           seats: int, is_available: int, description: str | None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Tour (name, cost, datetimeStart, datetimeEnd,
                          seats, isAvailable, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, cost, datetime_start, datetime_end,
          seats, is_available, description))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


# ---------- Read ----------

def get_by_id(tour_id: int) -> Tour | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE tourID = ?", (tour_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Tour]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY datetimeStart")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_available() -> list[Tour]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE isAvailable = 1 ORDER BY datetimeStart")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


# ---------- Update ----------

def update(tour_id: int, name: str, cost: float, datetime_start: str,
           datetime_end: str, seats: int, is_available: int,
           description: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Tour
        SET name = ?,
            cost = ?,
            datetimeStart = ?,
            datetimeEnd = ?,
            seats = ?,
            isAvailable = ?,
            description = ?
        WHERE tourID = ?
    """, (name, cost, datetime_start, datetime_end,
          seats, is_available, description, tour_id))
    conn.commit()
    conn.close()


# ---------- Delete ----------

def delete(tour_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Tour WHERE tourID = ?", (tour_id,))
    conn.commit()
    conn.close()
