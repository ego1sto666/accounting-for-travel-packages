"""Работа с таблицей Booking: CRUD-операции."""

from constants import STATUS_CANCELLED, STATUS_CREATED
from database.database import get_connection
from models.booking import Booking

# Бронь + название статуса, название и цена тура, логин клиента
_SELECT = """
    SELECT b.bookingID,
           b.tourID,
           b.userID,
           b.statusID,
           b.datetimeBooking,
           s.name,
           t.name,
           t.cost,
           u.login
    FROM Booking b
    JOIN BookingStatus s ON s.statusID = b.statusID
    JOIN Tour t ON t.tourID = b.tourID
    JOIN User u ON u.userID = b.userID
"""


def _map(row) -> Booking:
    return Booking(*row)


# ---------- Create ----------

def create(tour_id: int, user_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Booking (tourID, userID, statusID, datetimeBooking)
        VALUES (?, ?, ?, strftime('%Y-%m-%d %H:%M', 'now', 'localtime'))
    """, (tour_id, user_id, STATUS_CREATED))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


# ---------- Read ----------

def get_by_id(booking_id: int) -> Booking | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE b.bookingID = ?", (booking_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY b.datetimeBooking DESC")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_user(user_id: int) -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        _SELECT + " WHERE b.userID = ? ORDER BY b.datetimeBooking DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def count_active_by_tour(tour_id: int) -> int:
    """Сколько мест в туре уже занято (все брони, кроме отмененных)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM Booking
        WHERE tourID = ? AND statusID != ?
    """, (tour_id, STATUS_CANCELLED))
    count = cur.fetchone()[0]
    conn.close()
    return count


def count_by_tour(tour_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Booking WHERE tourID = ?", (tour_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count


def count_by_user(user_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Booking WHERE userID = ?", (user_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count


# ---------- Update ----------

def update_status(booking_id: int, status_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Booking SET statusID = ? WHERE bookingID = ?",
        (status_id, booking_id),
    )
    conn.commit()
    conn.close()


# ---------- Delete ----------

def delete(booking_id: int):
    """Физическое удаление. В программе брони не удаляются, а отменяются
    (логическое удаление через статус), чтобы сохранялась история."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Booking WHERE bookingID = ?", (booking_id,))
    conn.commit()
    conn.close()
